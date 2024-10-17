import cv2
import numpy as np
import time
import math
import os
import time
from skimage.metrics import structural_similarity as ssim

from Lib.Decorators.wrapper import _timing


file_path = os.path.join('/home/innotech/Project/Filler/Filler_robot/NeuroModules/models', 'coco.txt')
file = open(file_path,"r")
classes = file.read().split('\n')


class Timer:
	def __init__(self):
		self.start_time = 0


	def start(self):
		self.start_time = time.time()	


	def is_time_passed(self, seconds):
		current_time = time.time()
		elapsed_time = current_time - self.start_time

		return elapsed_time >= seconds
	

class Neuron:
	def __init__(self):
		self.connect_0 = None

		self.timer = Timer()

		file_path = os.path.join('/home/innotech/Project/Filler/Filler_robot/NeuroModules/models', 'yolov5n.onnx')
		self.net_v5 = cv2.dnn.readNetFromONNX(file_path)
		# self.net_v5.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
		# self.net_v5.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
		
		self.mode = 0
		
		self.threshold = 0.4
		self.nmsthreshold = 0.4

		self.list_find = {'cup': True, 'CUP': True, 'vase': True, 'wine glass': True, 'toilet': True, 'person': True}
		
		self.position = 0
		self.next_position_0 = True
		self.next_position_1 = False
		self.next_position_2 = False
		self.next_position_list = []
		
		self.limit_xmin = 30
		self.limit_xmax = 640 - 50
		self.limit_ymin = 0
		self.limit_ymax = 300
		
		self.factor_x = 9
		self.factor_y = 0.1
		self.perspective = 0

		self.objects_all = []
        
		self.memory_objects = []
		self.objects = []
			
		self.list_coord = []

		self.objects_filter = []
		
		self.region_x = 12
		self.region_y = 12
		self.leen = 1800
		
		self.hands_data = []
		self.hands_found = False

		self.id = 0
   

	def running(self):
		self.neuron_vision()

	
	def forget(self):
		self.objects_all = []
		self.memory_objects = []
		self.objects = []
		self.objects_filter = []
		self.list_coord = []

		#print('ЗАБЫЛ')
	

	def neuron_vision(self):
		self.threshold = 0.4
		self.nmsthreshold = 0.4

		if self.connect_0.interface != None:
			self.id = 0
			data = []

			cadr_1 = self.connect_0.camera.read_cam()
			
			self.connect_0.camera.running()
			tuple_obj = self.find_objects()
			data.append(tuple_obj)
			self.connect_0.interface.running()

			self.connect_0.camera.running()
			tuple_obj = self.find_objects()
			data.append(tuple_obj)
			self.connect_0.interface.running()

			self.connect_0.camera.running()
			tuple_obj = self.find_objects()
			data.append(tuple_obj)
			self.connect_0.interface.running()
		
			sorted_data = sorted(data, key=lambda x: x[1])
			max_value_second = max(sorted_data, key=lambda x: x[1])[1]
			filtered_data = [item for item in sorted_data if item[1] == max_value_second]
			sorted_filtered_data = sorted(filtered_data, key=lambda x: x[2])
			max_value_third = max(sorted_filtered_data, key=lambda x: x[2])

			self.objects_filter = max_value_third[0]

			lenght_1 = 0
			for obj in self.objects_filter:
				lenght_1 += obj[7]

			lenght_2 = 0
			for obj in self.memory_objects:
				lenght_2 += obj[7]

			#print('abs(lenght_1 - lenght_2)', abs(lenght_1 - lenght_2))

			if abs(lenght_1 - lenght_2) >= 50:
				self.memory_objects = self.objects_filter

			if len(self.objects_filter) <= len(self.memory_objects):
				self.memory_objects = self.objects_filter

			if len(self.objects_filter) <= len(self.memory_objects):
				self.memory_objects = self.objects_filter

			self.list_coord = self.pixel_to_coord(self.objects_filter)

			if len(self.list_coord) == 0:
				self.forget()


	def find_objects(self):
		objects_list = self.detect_v5(self.connect_0.camera.image_out)
		self.objects_filter = self.filter(objects_list)

		self.list_coord = self.pixel_to_coord(self.objects_filter)

		lenght = len(self.objects_filter)
		self.id += 1

		return (self.objects_filter, lenght, self.id)

	
	def detect_v5(self, image):
		self.objects_all = []

		if isinstance(image, np.ndarray):
			img_width, img_height = image.shape[1], image.shape[0]

			x_scale = img_width / 640
			y_scale = img_height / 640

			blob = cv2.dnn.blobFromImage(image, scalefactor=1/255, size=(640, 640), mean=[0, 0, 0], swapRB=True, crop=False)
			self.net_v5.setInput(blob)
			detections = self.net_v5.forward()[0]

			classes_ids = []
			confidences = []
			boxes = []
			rows = detections.shape[0]

			for i in range(rows):
				row = detections[i]
				confidence = row[4]
				if confidence > self.threshold:
					classes_score = row[5:]
					ind = np.argmax(classes_score)
					if classes_score[ind] > 0.5:
						classes_ids.append(ind)
						confidences.append(confidence)
						cx, cy, w, h = row[:4]
						x1 = int((cx - w / 2) * x_scale)
						y1 = int((cy - h / 2) * y_scale)
						width = int(w * x_scale)
						height = int(h * y_scale)
						box = np.array([x1, y1, width, height])
						boxes.append(box)

			indices = cv2.dnn.NMSBoxes(boxes, confidences, self.threshold, self.nmsthreshold)

			if isinstance(indices, np.ndarray):
				for i in indices:
					id_obj = 0
					ready = False

					x1, y1, w, h = boxes[i]
					label = classes[classes_ids[i]]
					conf = confidences[i]

					yr_center = int(y1 + w * (y1 + h) / self.leen)
					xr_center = int(x1 + w / 2)

					self.perspective = abs(xr_center - img_width / 2) * 1 / self.factor_x

					# print('H', h)

					if h <= 190:
						xd = -2
						yd = -7
					else:
						xd = 6
						yd = 7

					w1 = int(w - self.perspective)
					
					if xr_center >= self.connect_0.camera.img_width / 2:
						xr_center_2 = int((xr_center - self.perspective * 2)) - xd 
					else:
						xr_center_2 = int((xr_center + self.perspective * 2)) + xd 

					
					yr_center_2 = int(((y1 + h) - w1 / 2 * 0.7) + (1 - abs(self.connect_0.camera.img_height - (y1 + h)) / 700)) + yd

					yr_center = int((y1 + w1 / 2 * 0.5 * (1 + h/1000)))

					self.objects_all.append([ready, id_obj, label, conf, x1, y1, w, h, xr_center, yr_center, self.perspective, xr_center_2, yr_center_2])
			else:
				self.objects_all = []

		return self.objects_all
	

	def compare_images_feature_matching(self, obj):
		x1 = obj[4]
		y1 = obj[5]
		w = obj[6]
		h = obj[7]
		xr_center = obj[8]
		yr_center = obj[9]	
		perspective = obj[10]
		xr_center_2 = obj[11]
		yr_center_2 = obj[12]
		
		image_1 = self.connect_0.camera.image_copy
		image_2 = self.connect_0.camera.read_cam()

		image_1_gray = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
		image_2_gray = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)

		image_1_gray = cv2.GaussianBlur(image_1_gray, (5, 5), 0)
		image_2_gray = cv2.GaussianBlur(image_2_gray, (5, 5), 0)

		image_1_gray = cv2.medianBlur(image_1_gray, 5)
		image_2_gray = cv2.medianBlur(image_2_gray, 5)

		# image_1_gray = image_1
		# image_2_gray = image_2

		cropped_image_1 = image_1_gray[y1 + abs(y1 - yr_center) + 30: y1 + h + 2, x1 + 10 : x1 + w - 10]
		cropped_image_2 = image_2_gray[y1 + abs(y1 - yr_center) + 30: y1 + h + 2, x1 + 10: x1 + w  - 10]

		current_dir = os.path.dirname(os.path.abspath(__file__))

		cv2.imwrite(os.path.join(current_dir, 'cropped_image.png'), cropped_image_1)
		cv2.imwrite(os.path.join(current_dir, 'cropped_image_2.png'), cropped_image_2)

		#sift = cv2.SIFT_create(nfeatures=1129, contrastThreshold=0.012, edgeThreshold=100)
		sift = cv2.SIFT_create(nfeatures=1129, contrastThreshold=0.007, edgeThreshold=100)

		kp1, des1 = sift.detectAndCompute(cropped_image_1, None)
		kp2, des2 = sift.detectAndCompute(cropped_image_2, None)

		#print('len(kp1)', len(kp1), len(kp2))

		cropped_image_1_with_keypoints = cv2.drawKeypoints(cropped_image_1, kp1, None, flags=cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
		cropped_image_2_with_keypoints = cv2.drawKeypoints(cropped_image_2, kp2, None, flags=cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)

		cv2.imwrite(os.path.join(current_dir, 'cropped_image_1_with_keypoints.png'), cropped_image_1_with_keypoints)
		cv2.imwrite(os.path.join(current_dir, 'cropped_image_2_with_keypoints.png'), cropped_image_2_with_keypoints)

		if len(kp2) >= len(kp1) * 0.5:
			#print('Стакан есть')
			return True
		else:
			#print('Стакан нету')
			return False


	def compare_images(self, obj):
		x1 = obj[4]
		y1 = obj[5]
		w = obj[6]
		h = obj[7]
		xr_center = obj[8]
		yr_center = obj[9]	
		perspective = obj[10]
		xr_center_2 = obj[11]
		yr_center_2 = obj[12]
		
		image_1 = self.connect_0.camera.image_copy
		image_2 = self.connect_0.camera.read_cam()

		image_1_gray = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
		image_2_gray = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)

		# image_1_gray = cv2.GaussianBlur(image_1_gray, (3, 3), 0)
		# image_2_gray = cv2.GaussianBlur(image_2_gray, (3, 3), 0)

		# image_1_gray = cv2.medianBlur(image_1_gray, 3)
		# image_2_gray = cv2.medianBlur(image_2_gray, 3)

		cropped_image_1 = image_1_gray[y1 + abs(y1 - yr_center) + 60: y1 + h + 2, x1 + 10 : x1 + w - 10]
		cropped_image_2 = image_2_gray[y1 + abs(y1 - yr_center) + 60: y1 + h + 2, x1 + 10: x1 + w  - 10]
		
		current_dir = os.path.dirname(os.path.abspath(__file__))

		cv2.imwrite(os.path.join(current_dir, 'cropped_image.png'), cropped_image_1)
		cv2.imwrite(os.path.join(current_dir, 'cropped_image_2.png'), cropped_image_2)

		if cropped_image_1.shape == cropped_image_2.shape:
			similarity, _  = ssim(cropped_image_1, cropped_image_2,  win_size=7, gradient=True, data_range=255, full=False)
			similarity = similarity * 100
		else:
			similarity = 0
		
		# print(f"Схожесть изображений: {similarity:.2f}%")

		if similarity >= 60:
			# print('Стакан есть')
			return True
		else:
			# print('Стакан нету')
			return False


	def filter(self, objects_list):
		objects_new = []
		
		objects = sorted(objects_list, key = lambda sublist: sublist[4])
			
		find = False
		
		for obj in objects:
			label = obj[2]
			
			xr_center = obj[11]
			yr_center = obj[12]

			find = self.list_find.get(label, False)
			
			if find == True:
				should_add = True

				if xr_center < 210 or xr_center > 440:
					print('X limit')
					continue

				#if yr_center < 345 or yr_center > 460:
				if yr_center > 460:
					print('Y limit')
					continue
			
				for prev_obj in self.memory_objects:
					prev_status = prev_obj[0]
					prev_xr_center = prev_obj[11]
					prev_yr_center = prev_obj[12]

					if abs(xr_center - prev_xr_center) <= self.region_x and abs(yr_center - prev_yr_center) <= self.region_y:
						if prev_status == True:
							obj[0] = True
							should_add = False
						else:
							obj[0] = False
							
						break 
								
				if should_add == True:
					objects_new.append(obj) 
				else:
					objects_new.append(prev_obj)
					
		objects_new = sorted(objects_new, key = lambda sublist: sublist[4])			

		id_objects = []
		id_obj = 1
		
		for obj in objects_new:
			obj[1] = id_obj
			id_obj += 1
			id_objects.append(obj)

		objects = id_objects
						
		# print('3 Filter  self.objects:', objects)

		return objects
	

	def pixel_to_coord(self, objects):
		list_coord = []

		img_width, img_height = self.connect_0.camera.img_width , self.connect_0.camera.img_height

		for obj in objects:
			x1 = obj[4]
			y1 = obj[5]
			w = obj[6]
			h = obj[7]
			xr_center = obj[8]
			yr_center = obj[9]	
			perspective = obj[10]
			xr_center_2 = obj[11]
			yr_center_2 = obj[12]

			x = x1
			y = y1
			z = h
			
			x = xr_center_2
			y = yr_center_2

			point = (x, y)
			point = self.connect_0.camera.perspective.transform_coord(point)
			point = self.connect_0.camera.perspective.scale(point)


			if point[0] <= self.connect_0.camera.img_width/2:
				dx = abs(x1 - xr_center)
			else:
				dx = abs(x1 + w - xr_center)


			x = round(point[0], 1)
			y = round(point[1], 1)

			z = h  / 19.2 
			z2 = z * (1 + abs(15.7 - y) * 0.04)

			z2 = round(z2, 1)

			dx = w / 19.2 * (1 + abs(15.7 - y) * 0.04)

			#print("dx", dx)

			z3 = z2
			dz = z3

			if z2 > 7.7:
				if dx < 7:
					z3 = z2 * 0.6

				dz = 7.7
			else:
				z3 = z2
				dz = z3


			v = (3.142 * (dx / 2) ** 2 * z3) / 2 * (1 - abs(self.connect_0.camera.img_width/2 - xr_center_2) / 250) * (1 - abs(dz - z3) / 21)
			v = round(v, 1)
			
			list_coord.append((x, y, z2, v))
			
		
		return list_coord

import cv2
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


from Lib.Decorators.wrapper import _timing

import numpy as np


def nothing(x):
	pass


class Interface(QObject):
	frame_captured = pyqtSignal(QPixmap)

	def __init__(self):
		super().__init__()

		self.connect_0 = None

		self.visual = True

		self.x = 0
		self.y = 0

		self.img_monitor = None

		self.point_calibr = [(), (), (), ()]

		self.mode = 1
		
		self.create_trackbar = False


	def _visual_line(func):
		def wrapper(*args):
			self = args[0]
			
			if self.visual == True:
				func(*args)
			
		return wrapper	
	
	
	# @_timing(True)	
	def running(self):
		self.save_image()
		# self.get_trackbar()

	
	def create_window(self):
		cv2.namedWindow( "Detect" )
		cv2.createTrackbar("x_point", "Detect" , self.connect_0.camera.point_pixel[0][0], self.connect_0.camera.img_width, nothing)
		cv2.createTrackbar("y_point", "Detect" , self.connect_0.camera.point_pixel[0][1], self.connect_0.camera.img_height, nothing)
		
		cv2.createTrackbar("point_1_x", "Detect" , self.connect_0.camera.point_pixel[0][0], self.connect_0.camera.img_width, nothing)
		cv2.createTrackbar("point_1_y", "Detect" , self.connect_0.camera.point_pixel[0][1], self.connect_0.camera.img_height, nothing)

		cv2.createTrackbar("point_2_x", "Detect" , self.connect_0.camera.point_pixel[1][0], self.connect_0.camera.img_width, nothing)
		cv2.createTrackbar("point_2_y", "Detect" , self.connect_0.camera.point_pixel[1][1], self.connect_0.camera.img_height, nothing)

		cv2.createTrackbar("point_3_x", "Detect" , self.connect_0.camera.point_pixel[2][0], self.connect_0.camera.img_width, nothing)
		cv2.createTrackbar("point_3_y", "Detect" , self.connect_0.camera.point_pixel[2][1], self.connect_0.camera.img_height, nothing) 

		cv2.createTrackbar("point_4_x", "Detect" , self.connect_0.camera.point_pixel[3][0], self.connect_0.camera.img_width, nothing)
		cv2.createTrackbar("point_4_y", "Detect" , self.connect_0.camera.point_pixel[3][1], self.connect_0.camera.img_height, nothing)

		cv2.createTrackbar("a", "Detect" , int(abs(self.connect_0.camera.perspective.a) * 100000), 9999, nothing)
		cv2.createTrackbar("b", "Detect" , int(abs(self.connect_0.camera.perspective.b) * 100000), 9999, nothing)

		self.get_trackbar()

		self.create_trackbar = True

  		
	def get_trackbar(self):
		self.x = cv2.getTrackbarPos("x_point", "Detect")
		self.y = cv2.getTrackbarPos("y_point", "Detect")

		self.x_1 = cv2.getTrackbarPos("point_1_x", "Detect")
		self.y_1 = cv2.getTrackbarPos("point_1_y", "Detect")

		self.x_2 = cv2.getTrackbarPos("point_2_x", "Detect")
		self.y_2 = cv2.getTrackbarPos("point_2_y", "Detect")

		self.x_3 = cv2.getTrackbarPos("point_3_x", "Detect")
		self.y_3 = cv2.getTrackbarPos("point_3_y", "Detect")

		self.x_4 = cv2.getTrackbarPos("point_4_x", "Detect")
		self.y_4 = cv2.getTrackbarPos("point_4_y", "Detect")

		# self.connect_0.camera.perspective.a = cv2.getTrackbarPos("a", "Detect") / 100000
		# self.connect_0.camera.perspective.b = -1 * cv2.getTrackbarPos("b", "Detect") / 100000
 
		self.point_calibr = [(self.x_1, self.y_1), (self.x_2, self.y_2), (self.x_3, self.y_3), (self.x_4, self.y_4)]

		self.connect_0.camera.perspective.write_point(self.point_calibr)


	# @_timing(True)			
	def show_img(self, image):
		img_copy = image.img.copy()
		
		self.draw_sight(img_copy)
		# self.draw_limit_line(img_copy)
		# self.draw_box_all(img_copy)
		self.draw_box(img_copy)
		# self.perspective(img_copy)

		# point = (self.x, self.y)
		# point = camera.perspective.transform_coord(point)

		# point = camera.perspective.scale(point)

		# camera.perspective.draw(img_copy)
		
		cv2.imshow("Detect", img_copy)
		cv2.waitKey(1)
		
		#print('image_show')
		
	
	def destroy_window(self):
		cv2.destroyAllWindows()

	
	def save_image(self):
		if isinstance(self.connect_0.camera.image_out, np.ndarray):

			match self.mode:
				case 0:
					pixmap = self.connect_0.camera.image_out

				case 1: 
					# self.get_trackbar()

					image_draw = self.draw_box(self.connect_0.camera.image_out, self.connect_0.neuron.objects_filter)

					# self.draw_box_all(image_draw)

					# cv2.circle(image_draw, (int(self.connect_0.camera.img_width/2), int(self.connect_0.camera.img_height/2)), 200, (255, 0, 255), 2)
					# cv2.circle(image_draw, (int(self.connect_0.camera.img_width/2), int(self.connect_0.camera.img_height/2)), 600, (255, 0, 255), 2)
					
					
					# center1 = (int(self.connect_0.camera.img_width/2), self.connect_0.camera.img_height - 150)  #   
					# axes1 = (210, 120)  #    
					# angle1 = 0  #    
					# startAngle1 = 0  #     
					# endAngle1 = 360  #     
					# color1 = (0, 255, 0) 
					# thickness1 = 2  #    
					
					# cv2.ellipse(image_draw, center1, axes1, angle1, startAngle1, endAngle1, color1, thickness1)
					
					# center1 = (int(self.connect_0.camera.img_width/2), self.connect_0.camera.img_height - 150)  #   
					# axes1 = (300, 210)  #    
					# angle1 = 0  #    
					# startAngle1 = 0  #     
					# endAngle1 = 360  #     
					# color1 = (0, 255, 0) 
					# thickness1 = 2  #    
					
					# cv2.ellipse(image_draw, center1, axes1, angle1, startAngle1, endAngle1, color1, thickness1)


					pixmap = image_draw
				
				case 2:
					if not self.create_trackbar:
						self.create_window()

					self.get_trackbar()

					image_draw = self.draw_box(self.connect_0.camera.image_out, self.connect_0.neuron.objects_filter)

					point = (self.x, self.y)
					point = self.connect_0.camera.perspective.transform_coord(point)

					point = self.connect_0.camera.perspective.scale(point)

					image_draw = self.connect_0.camera.perspective.draw(image_draw)

					pixmap = image_draw


			img_monitor = pixmap[160:530,:]
			h, w, ch = img_monitor.shape
		

			q_image = QImage(img_monitor.data.tobytes(), w, h, ch * w, QImage.Format_BGR888)
			q_image = q_image.scaled(720, 480, Qt.KeepAspectRatio)

			pixmap = QPixmap.fromImage(q_image)

			self.frame_captured.emit(pixmap)

		
	
	def draw_sight(self, img):
		size = 300
	
		# cv2.line(img, (int(camera.img_width/2), int(camera.img_height/2) - size), (int(camera.img_width/2 ) , int(camera.img_height/2) + size), (0, 0, 0), 2)
		# cv2.line(img, (int(camera.img_width/2) - size, int(camera.img_height/2)), (int(camera.img_width/2) + size, int(camera.img_height/2)), (0, 0, 0), 2)
		
		cv2.line(img, (int(self.connect_0.camera.img_width/2), int(self.connect_0.camera.img_height/2) - size), (int(self.connect_0.camera.img_width/2 ) , int(self.connect_0.camera.img_height/2) + size), (0, 0, 0), 2)
		cv2.line(img, (int(self.connect_0.camera.img_width/2) - size, int(self.connect_0.camera.img_height/2)), (int(self.connect_0.camera.img_width/2) + size, int(self.connect_0.camera.img_height/2)), (0, 0, 0), 2)

		return img


	def line_h(self, img, h):
		for i in range(20):
			cv2.line(img, (0, int(i * h)), (self.connect_0.camera.img_width , int(i * h)), (120, 120, 120), 1)
		
		return img

	# def perspective(self, img):
	# 	cv2.circle(img, (self.x, self.y), 5, (255, 0, 255), -1)
		

	# @_visual_line
	# def draw_limit_line(self, img):
	# 	cv2.line(img, (neuron.limit_xmin, 0), (neuron.limit_xmin, camera.img_height), (255, 0, 0), 1)
	# 	cv2.line(img, (neuron.limit_xmax, 0), (neuron.limit_xmax, camera.img_height), (255, 0, 0), 1)
		
	# 	cv2.line(img, (0, neuron.limit_ymax), (camera.img_width, neuron.limit_ymax), (255, 0, 0), 1)

		
	def draw_box(self, image, objects):
		i = 0

		if objects != None:
			for obj in objects:
				ready = obj[0]
				id_obj = obj[1]
				label = obj[2]
				conf = obj[3]
				x1 = obj[4]
				y1 = obj[5]
				w = obj[6]
				h = obj[7]
				xr_center = obj[8]
				yr_center = obj[9]
				perspective = obj[10]
				xr_center_2 = obj[11]
				yr_center_2 = obj[12]
				
				if ready == False:
					color_box = (255, 0, 0)
				else:
					color_box = (0, 0, 255)	

				#print('wfwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww', camera.perspective_transformed([neuron.list_coord[i][0] * 10, neuron.list_coord[i][1] * 10]), neuron.list_coord[i][0] * 10, neuron.list_coord[i][1] * 10)

				text = f'{id_obj}' + ':' + label + ' ' + f'{ready}'

				text = f'{id_obj}: {label}' 

				cv2.rectangle(image,(x1, y1),(x1 + w, y1 + h), color_box, 2)
				cv2.putText(image, text, (x1, y1 + h + 15), cv2.FONT_HERSHEY_COMPLEX, 0.7, color_box, 1)

				cv2.rectangle(image, (int(xr_center - 4), yr_center - 4),(int(xr_center + 4), yr_center + 4), (255, 255, 0), -1)
				cv2.rectangle(image, (int(xr_center - self.connect_0.neuron.region_x), yr_center - self.connect_0.neuron.region_y),(int(xr_center + self.connect_0.neuron.region_x), yr_center + self.connect_0.neuron.region_y), (0, 255, 0), 1)
				
				cv2.rectangle(image, (int(xr_center_2 - 4), yr_center_2 - 4),(int(xr_center_2 + 4), yr_center_2 + 4), (255, 255, 0), -1)

				cv2.putText(image, f'{self.connect_0.neuron.list_coord[i]}', (x1, y1 + h + 32), cv2.FONT_HERSHEY_COMPLEX, 0.5, color_box, 1)

				cv2.line(image, (x1, yr_center), (x1 + w, yr_center), (255, 255, 0), 1)
				
				#cv2.line(image, (int(xr_center), yr_center), (int(xr_center - perspective * 4), y1 + h), (255, 255, 0), 1)

				cv2.line(image, (int(xr_center), yr_center), (int(xr_center_2), yr_center_2), (255, 255, 0), 1)

				i += 1
		
		return image


	def draw_box_all(self, img):
		objects = self.connect_0.neuron.objects_all

		i = 0
		
		for obj in objects:
			ready = obj[0]
			id_obj = obj[1]
			label = obj[2]
			conf = obj[3]
			x1 = obj[4]
			y1 = obj[5]
			w = obj[6]
			h = obj[7]
			xr_center = obj[8]
			yr_center = obj[9]
			perspective = obj[10]
			xr_center_2 = obj[11]
			yr_center_2 = obj[12]
			
			label_person = 'PERSON'
				
			color_box = (0, 255, 0)	
			color_text = (0, 90, 0)	

			#print('wfwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww', camera.perspective_transformed([neuron.list_coord[i][0] * 10, neuron.list_coord[i][1] * 10]), neuron.list_coord[i][0] * 10, neuron.list_coord[i][1] * 10)

			if label == 'cocperson':
				cv2.rectangle(img,(x1, y1),(x1 + w, y1 + h), color_box, 2)
				cv2.putText(img, f'{label_person}', (x1, y1 - 2), cv2.FONT_HERSHEY_COMPLEX, 0.7, color_text, 1)

			#cv2.rectangle(img, (int(xr_center - 4), yr_center - 4),(int(xr_center + 4), yr_center + 4), (255, 255, 0), -1)
			#cv2.rectangle(img, (int(xr_center - neuron.region_x), yr_center - neuron.region_y),(int(xr_center + neuron.region_x), yr_center + neuron.region_y), (0, 255, 0), 1)
			
			#cv2.rectangle(img, (int(xr_center_2 - 4), yr_center_2 - 4),(int(xr_center_2 + 4), yr_center_2 + 4), (255, 255, 0), -1)

			#cv2.putText(img, f'{neuron.list_coord[i]}', (x1 - 20, y1 - 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 0), 1)

			#cv2.line(img, (x1, yr_center), (x1 + w, yr_center), (255, 255, 0), 1)
			
			#cv2.line(img, (int(xr_center), yr_center), (int(xr_center - perspective * 4), y1 + h), (255, 255, 0), 1)

			#cv2.line(img, (int(xr_center), yr_center), (int(xr_center_2), yr_center_2), (255, 255, 0), 1)

			#i += 1
			
# interface = Interface()
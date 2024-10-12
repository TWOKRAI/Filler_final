import asyncio
import math
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject

from Filler_robot.MotorModules.motor import Motor
from Raspberry.pins_table import pins

#from Lib.Decorators.wrapper import _timing

from Filler_interface.app import app


class Axis:
	def __init__(self, name_axis, motor):
		self.print_on = True

		self.name_axis = name_axis

		self.motor = motor

		self.distance_move = 0
		self.ready = False

		self.limit_min = 0
		self.limit_max = 0
		self.error_limit = False

		self.arm_lenght = 1

		self.angle_0 = 0
		self.angle = 0
		self.delta_angle = 0
		self.step_angle = 0.15

		self.step_distance = 0

		self.direction_real = True
		self.direction_distance = True

		self.x0 = 0
		self.y0 = 0
		self.z0 = 0
		self.x = 0
		self.y = 0
		self.z = 0

		self.d1 = 0

	
	def angle_real(self):
		if self.direction_real:
			angle_real = self.angle_0 - self.motor.value * self.step_angle
		else:
			angle_real = self.angle_0 - self.motor.value * self.step_angle

		# print(f'angle_real {self.name_axis}: {angle_real}')
		# print(f'angle_real {self.name_axis} motor value: {self.motor.value}')

		return angle_real


	def distance_angle(self, angle):
		delta_angle = self.angle_real() - angle

		delta_angle = round(delta_angle, 1)

		return delta_angle


	def angle_to_step(self, angle):
	# 	if self.print_on: 
	# 		print('angle_to_step, input:', angle)

		delta_angle = self.distance_angle(angle)
		distance = delta_angle / self.step_angle

		# if self.print_on: 
		# 	print('angle_to_step',self.name_axis, angle, 'distance_angle', delta_angle, 'distance', distance)
		# 	print()

		return distance
	


class Robot_module(QObject):
	block_data_on = pyqtSignal()
	block_data_off = pyqtSignal()
	update_data = pyqtSignal()

    
	def __init__(self):
		super().__init__()

		self.connect_0 = None

		self.start = False

		self.print_on = False

		self.first_go = False

		self.calibration_ready = False
		self.calib_distance = 1000

		self.stopped = False

		self.lenght_filler = 4.5

		self.step_position_value = 300
		self.step_position = 0

		self.radius_min = 15
		self.radius_max = 27

		self.pumping_find = False
		self.find = False

		self.home = False

		self.move_home = False

		self.error_x = False
		self.error_y = False
		self.error_z = False

		self.joker = 0

		self.button_stop = False

		self.motor_x = Motor('x', pins.motor_x_step, pins.motor_x_dir, pins.motor_x_enable)
		self.motor_y = Motor('y', pins.motor_y_step, pins.motor_y_dir, pins.motor_y_enable)
		self.motor_z = Motor('z', pins.motor_z_step, pins.motor_z_dir, pins.motor_z_enable)

		self.distance_x = 0
		self.distance_y = 0
		self.distance_z = 0

		self.axis_x = Axis('motor_x', self.motor_x)
		self.axis_x.motor.enable_on(False)
		self.axis_x.motor.speed_default = 0.00007
		self.axis_x.motor.speed_def = 0.00007
		self.axis_x.motor.direction = False
		self.axis_x.step_angle = 0.04
		self.axis_x.angle_0 = 0
		self.axis_x.angle = self.axis_x.angle_0
		self.axis_x.limit_min = -90
		self.axis_x.limit_max = 90
		

		self.axis_y = Axis('motor_y', self.motor_y)
		self.axis_y.motor.enable_on(False)
		self.axis_y.motor.speed_default = 0.00007
		self.axis_y.motor.speed_def = 0.00007
		self.axis_y.motor.direction = False
		self.axis_y.step_angle = 0.123
		self.axis_y.arm_lenght = 12
		self.axis_y.angle_0 = 124
		self.axis_y.angle = self.axis_y.angle_0
		self.axis_y.y0 = 0
		self.axis_y.z0 = 22.5
		self.axis_y.limit_min = 7
		self.axis_y.limit_max = 130
		

		self.axis_z = Axis('motor_z', self.motor_z)
		self.axis_z.motor.enable_on(False)
		self.axis_z.motor.speed_default = 0.00007
		self.axis_z.motor.speed_def = 0.00007
		self.axis_z.motor.direction = True
		self.axis_z.direction_real = False
		self.axis_z.direction_distance = False
		self.axis_z.step_angle = 0.123
		self.axis_z.arm_lenght = 12
		self.axis_z.angle_0 = 145
		self.axis_z.angle = self.axis_z.angle_0
		self.axis_z.limit_min = 145
		self.axis_z.limit_max = 95
		
		self.time_start_x = 0
		self.time_start_y = 0
		self.time_start_z = 0

		self.enable_status = False

		#self.connect_0.laser.laser_on = False
		

	def running(self):
		self.move_objects()

	
	def enable_motors(self, value = False):
		self.axis_x.motor.enable_on(value)
		self.axis_y.motor.enable_on(value)
		self.axis_z.motor.enable_on(value)
		
		self.enable_status = value

	
	def stop_motors(self):
		self.block_data_off.emit()

		# self.connect_0.pump_station.enable_motors(False)
		# self.connect_0.pump_station.motor_1.stop_for = True
		# self.connect_0.pump_station.motor_2.stop_for = True

		self.stopped = True

		self.start = False

		self.axis_x.motor.stop = True
		self.axis_y.motor.stop = True
		self.axis_z.motor.stop = True

		self.button_stop = True

		self.calibration_ready = False

	
	def no_stop_motors(self):
		self.block_data_off.emit()

		self.stopped = False

		self.connect_0.pump_station.pump_1.motor.stop = False
		self.connect_0.pump_station.pump_2.motor.stop = False

		self.axis_x.motor.stop = False
		self.axis_y.motor.stop = False
		self.axis_z.motor.stop = False

		self.button_stop = False


	def null_value(self):
		self.axis_x.motor.null_value()
		self.axis_y.motor.null_value()
		self.axis_z.motor.null_value()

		self.distance_x = 0
		self.distance_y = 0
		self.distance_z = 0

		self.distance_x_end = 0
		self.distance_y_end = 0
		self.distance_z_end = 0


	def angle_to_coord(self, angle_x, angle_y, angle_z):
		x = 0
		y = 0
		z = 0

		error_limit_x = False
		error_limit_y = False
		error_limit_z = False

		angle_x1 = angle_x
		angle_y1 = angle_y
		angle_z1 = angle_z

		if angle_x < self.axis_x.limit_min:
			angle_x = self.axis_x.limit_min
			error_limit_x = True

		if angle_x > self.axis_x.limit_max:
			angle_x = self.axis_x.limit_max
			error_limit_x = True

		if angle_y < self.axis_y.limit_min:
			angle_y = self.axis_y.limit_min
			error_limit_y = True

		if angle_y > self.axis_y.limit_max:
			angle_y = self.axis_y.limit_max
			error_limit_y = True

		#print(angle_z, self.axis_z.limit_min)
		if angle_z > self.axis_z.limit_min:
			angle_z = self.axis_z.limit_min
			error_limit_z = True

		if self.axis_z.angle >= 60:
			limit_z2 = self.axis_z.angle_0 - angle_y 
		else:
			limit_z2 = 60

		#print(angle_z, self.axis_z.limit_max - limit_z2,  limit_z2)
		if angle_z < self.axis_z.limit_max - limit_z2:
			angle_z = self.axis_z.limit_max + limit_z2
			error_limit_z = True


		#print(angle_x1, angle_y1, angle_z1)

		y1 = self.axis_y.y0 + self.axis_y.arm_lenght * math.cos(math.radians(angle_y1))
		z1 = self.axis_y.z0 + self.axis_y.arm_lenght * math.sin(math.radians(angle_y1))

		#print(round(x, 5), round(y1, 5), round(z1, 5))

		y2 = y1 + self.axis_z.arm_lenght * math.cos(math.radians(angle_z1 - angle_y))
		z2 = z1 - self.axis_z.arm_lenght * math.sin(math.radians(angle_z1 - angle_y))


		#print(round(x, 5), round(y2, 5), round(z2, 5))

		x3 = (y2 + self.lenght_filler) * math.sin(math.radians(angle_x1))
		y3 = (y2 + self.lenght_filler) * math.cos(math.radians(angle_x1)) 
		z3 = z2

		x = round(x3, 3)
		y = round(y3, 3)
		z = round(z3, 3)

		#print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz', x, y, z, error_limit_x, error_limit_y, error_limit_z)

		return x, y, z, error_limit_x, error_limit_y, error_limit_z
	

	#@_timing(True)
	def find_angle(self, x0, y0, z0):
		angle_x = self.axis_x.angle_0
		angle_y = self.axis_y.angle_0
		angle_z = self.axis_z.angle_0

		h = 1
		i = 0

		error = False

		while True:
			x, y, z, error_limit_x, error_limit_y, error_limit_z = self.angle_to_coord(angle_x, angle_y, angle_z)

			if y <= y0:
				if error_limit_y == False:
					angle_y -= 1* h

				if error_limit_z == False:
					angle_z -= 1 * h
			else:
				h = 0.1

				if error_limit_x == False:
					if x0 > 0:
						if x < x0:
							angle_x += 1 * h
					elif x0 < 0:
						if x > x0:
							angle_x -= 1 * h
			
				if abs(x) >= abs(x0):
					if z <= z0:
						if error_limit_y == False:
							angle_y -= 1 * h

						if error_limit_z == False:
							angle_z -= 2 * h
					else:

						angle_y += 1 * h

						angle_z += 2 * h
					
			if error_limit_y == True:
				angle_y += 1
				angle_z -= 1

			i += 1
			#print(i)
			
			if abs(x) >= abs(x0) and y >= y0 and z <= z0:
				break

			if i > 100000:
				error = True
				print('Error position', abs(x) >= abs(x0), y >= y0, z <= z0)
				break

		angle_x = round(angle_x, 3)
		angle_y = round(angle_y, 3)
		angle_z = round(angle_z, 3)

		# print(f"angle_x: {angle_x} x: {x}")
		# print(f"angle_y: {angle_y} y: {y}")
		# print(f"angle_z: {angle_z} z: {z}")
		# print('x0, y0, z0', x0, y0, z0)

		return angle_x, angle_y, angle_z, error


	def steps_find(self, angle_y, angle_z):
		delta_y = self.axis_y.distance_angle(angle_y)

		angle_real = self.axis_z.angle_0 - self.axis_z.motor.value * self.axis_z.step_angle


		# print('self.axis_z.motor.value', self.axis_z.motor.value)
		# self.axis_z.motor.value = (self.axis_z.motor.value * self.axis_z.step_angle + delta_y) / self.axis_z.step_angle 
		# print('self.axis_z.motor.value2', self.axis_z.motor.value)

		#print('angle_real', angle_real, angle_z)
	
		
		new_angle_z = angle_real - delta_y

		if new_angle_z < 35:
			new_angle_z = 35
		

		#print('new_angle_z, angle_z', new_angle_z, angle_z)

		delta_z = abs(new_angle_z - angle_z)


		if new_angle_z < angle_real:
			delta_z = delta_z
		else:
			delta_z = -delta_z


		# print('delta_z', delta_z)

		distante_z = delta_z / self.axis_z.step_angle

		return distante_z
		

	async def _detect_sensor(self):
		while not self.button_stop:
			if self.stopped:
				break

			switch_y = pins.switch_y.get_value()

			if switch_y:
				self.axis_y.motor.stop = True
				self.axis_y.motor.ready = True
				break
				
			await asyncio.sleep(0.01)

	
	async def _limit(self):

		while True:
			if self.stopped:
				break

			# if self.axis_y.motor.value <= 300 and self.axis_y.motor.ready == False:
			# 	self.axis_z.motor.stop_for = True
			# else:
			# 	self.axis_z.motor.stop_for = False
			
			await asyncio.sleep(0.001)


	async def _move_async(self, distance_x, distance_y, distance_z, detect = False):
		#self.block_data_on.emit()

		self.stopped = False
		tasks = []

		if detect:
			tasks.append(asyncio.create_task(self._detect_sensor()))

		# if self.move_home:
		# 	tasks.append(asyncio.create_task(self._no_enabel_z()))

		# tasks.append(asyncio.create_task(self._limit()))

		if distance_x != 0:
			tasks.append(asyncio.create_task(self.axis_x.motor.move(distance_x, async_mode=True, time_start = self.time_start_x)))
		
		if distance_y != 0:
			tasks.append(asyncio.create_task(self.axis_y.motor.move(distance_y, async_mode=True, time_start = self.time_start_y)))

		if distance_z != 0 and self.move_home == False:
			tasks.append(asyncio.create_task(self.axis_z.motor.move(distance_z, async_mode=True, time_start = self.time_start_z)))
			
		try:
			await asyncio.gather(*tasks)
		except asyncio.CancelledError:
			for task in tasks:
				if not task.done():
					task.cancel()

		self.stopped = True

		self.time_start_x = 0
		self.time_start_y = 0
		self.time_start_z = 0

		self.move_home = False

		self.block_data_off.emit()

		# if detect:
		# 	sensor_task.cancel()
		
		# limit_task.cancel()


	def move(self, distance_x, distance_y, distance_z, detect = False):
		self.connect_0.laser.on_off(0)
		
		# speed = (10 - app.window_robot.speed_robot) / 5000
		# speed = round(speed, 6)

		# speed = app.window_robot.speed_robot

		speed = (100 - app.window_robot.speed_robot) / 50000
		speed = round(speed, 6)

		self.axis_x.motor.speed_def = self.axis_x.motor.speed_default + speed
		self.axis_y.motor.speed_def = self.axis_y.motor.speed_default + speed
		self.axis_z.motor.speed_def = self.axis_z.motor.speed_default + speed
		
		asyncio.run(self._move_async(distance_x, distance_y, distance_z, detect))
		

	def go_to_point(self, x, y, z):
		if self.print_on: 
			print('go_to_point, input:', 'x, y, z', x, y, z)
			print()
		
		angle_x0 = self.axis_x.angle_real()
		angle_y0 = self.axis_y.angle_real()
		angle_z0 = self.axis_z.angle_real()

		x0, y0, z0, _, _, _ = self.angle_to_coord(angle_x0, angle_y0, angle_z0)
		# if self.print_on:
			# print('go_to_point', 'x0, y0, z0', x0, y0, z0)
			# print('go_to_point', 'angle_x0, angle_y0, angle_z0', angle_x0, angle_y0, angle_z0)
			# print()

		angle_x, angle_y, angle_z, error = self.find_angle(x, y, z)
		# if self.print_on:
		# 	print('go_to_point, self.find_angle', 'angle_x, angle_y, angle_z,', angle_x, angle_y, angle_z)

		x1, y1, z1, _, _, _ = self.angle_to_coord(angle_x, angle_y, angle_z)
		if self.print_on:
			print('go_to_point','proverka' , 'x, y, z', x1, y1, z1)
			print()

		error_x = abs(x1 - x)
		error_y = abs(y1 - y)
		error_z = abs(z1 - z)

		if self.print_on:
			print('go_to_point','error', 'error_x, error_y, error_z', error_x, error_y, error_z)
			print()
	

		if error_x > 1 or error_y > 1 or error_z > 1:
			pass

		
		self.distance_x = self.axis_x.angle_to_step(angle_x) #+150 
		self.distance_y = self.axis_y.angle_to_step(angle_y)
		self.distance_z = self.steps_find(angle_y, angle_z)

		# if self.home == False:
		# 	self.distance_z = self.steps_find(angle_y, angle_z)
		# else:
		# 	self.distance_z = self.axis_z.angle_to_step(angle_z)

		# self.home = False

		if self.print_on:
			print('go_to_point', 'distance_x, distance_y, distance_z', self.distance_x, self.distance_y, self.distance_z)
			print()

		# input('GO???')


		self.distance_x_end = self.distance_x
		self.distance_y_end = self.distance_y
		self.distance_z_end = self.distance_z


		self.time_start_z = 0.5
	
		self.move(self.distance_x, self.distance_y, self.distance_z)
		
		if self.print_on:
			print('go_to_point Приехал в координаты:', 
				'x:', x1, 'angle x:', self.axis_x.angle_real(),
				'y:', y1, 'angle y:', self.axis_y.angle_real(), 
				'z:', z1, 'angle z:', self.axis_z.angle_real())


	def check_limit(self, x, y, z):
		limit_check = False

		radius = math.sqrt((x**2) + (y**2))

		if self.radius_min <= radius <= self.radius_max and -15 <= x <= 15:
			limit_check = True
		else:
			limit_check = False

		# if self.print_on:
		# 	print('check_limit radius', radius, limit_check)

		return limit_check


	def move_objects(self, pumping = False):
		switch_y = pins.switch_y.get_value()

		if not switch_y and self.button_stop == False:
			#print('Не на свитче Y')
			self.calibration()

		if not self.calibration_ready and self.button_stop == False:
			self.calibration()

		
		list_objects = self.connect_0.neuron.objects_filter
		list_coord = self.connect_0.neuron.list_coord

		if self.print_on:
			print('move_objects list_objects', list_objects)
	
			print('move_objects list_coord', list_coord)

		i = 0
		limit = False

		completed = False

		for coord in list_coord:
			if self.start == False and self.pumping_find == False:
				break

			self.enable_motors(True)
			
			x, y, z, v = coord

			# if z > 12:
			# 	z = z + 3

			z = z + 2

			if z > 13: 
				z = z + 2

			
			if y > 14:
				y = y * (1 - abs(14 - y) /140)
				x = x * (1 - abs(14 - y) /140)

			if z > 14:
				y = y * 1.05
				x = x * 0.9

			# x = x * 0.9
			# y = y * 0.9

			limit = self.check_limit(x, y, z)

			if list_objects[i][0] == False and limit == True: 
				# z = z + 2
				
				self.enable_motors(True)

				if self.joker >= 2:
					self.joker_move()
					list_objects[i][0] = True
					self.connect_0.neuron.memory_objects = list_objects
					self.joker = 0
					continue
					
				self.go_to_point(x, y, z)

				# self.connect_0.neuron.find_objects()
				
				if self.button_stop == False:
					if app.window_robot.presence_cup == 1:
						presence = self.connect_0.neuron.compare_images_feature_matching(list_objects[i])
					else:
						presence = True

					if presence:
						if self.pumping_find:
							self.find = True
							break

						if self.start == False:
							break
						
						self.connect_0.pump_station.cap_value = v
						self.connect_0.pump_station.filler()
						completed = True
						list_objects[i][0] = True
						self.connect_0.neuron.memory_objects = list_objects
					else:
						self.joker += 1


					self.connect_0.interface.save_image()

					self.go_home()

			i += 1

		if not self.start and not self.pumping_find:
			self.go_home()

		if completed and not self.pumping_find and self.start:
			self.connect_0.laser.on_off(0)
			time_wait = app.window_robot.time_robot * 1000
			QThread.msleep(time_wait)
		

	async def _detect_switch_x(self):
		while not self.button_stop:
			switch_x = pins.switch_x.get_value()

			if switch_x:
				raise asyncio.CancelledError()

			await asyncio.sleep(0.001)


	async def _calibration_x_async(self):
		tasks = []

		distance_x = -3000
		
		tasks.append(asyncio.create_task(self._detect_switch_x()))
		tasks.append(asyncio.create_task(self.axis_x.motor.move(distance_x, async_mode=True)))
			

		try:
			await asyncio.gather(*tasks)
		except asyncio.CancelledError:
			for task in tasks:
				if not task.done():
					task.cancel()
	
	
	async def _detect_switch_y(self):
		while not self.button_stop:
			switch_y = pins.switch_y.get_value()

			if switch_y:
				raise asyncio.CancelledError()

			await asyncio.sleep(0.001)


	async def _calibration_y_async(self):
		tasks = []

		distance_y = -3000
		
		tasks.append(asyncio.create_task(self._detect_switch_y()))
		tasks.append(asyncio.create_task(self.axis_y.motor.move(distance_y, async_mode=True)))
			

		try:
			await asyncio.gather(*tasks)
		except asyncio.CancelledError:
			for task in tasks:
				if not task.done():
					task.cancel()


	def calibration(self):
		self.connect_0.laser.on_off(0)

		if self.button_stop == False:
			self.axis_x.motor.enable_on(True)
			self.axis_y.motor.enable_on(True)
			self.axis_z.motor.enable_on(False)

			QThread.msleep(1000)
			
			self.go_home_marker = True

			switch_y = pins.switch_y.get_value()
			if switch_y:
				self.axis_y.motor.speed_def = 0.002
				self.axis_y.motor.move(210)

				self.axis_y.motor.speed_def = 0.0007
				self.axis_z.motor.enable_on(False)
				
			
			asyncio.run(self._calibration_y_async())

			self.move(0, -10, 0)

			asyncio.run(self._calibration_x_async())
			self.move(790, 0, 0)

			self.null_value()

			self.calibration_ready = True

			self.enable_motors(False)


	async def _no_enabel_z(self):
		for _ in range(4):
			self.axis_z.motor.enable_on(False)
			await asyncio.sleep(0.1)
			self.axis_z.motor.enable_on(True)
			await asyncio.sleep(0.2)
		
		self.axis_z.motor.enable_on(False)


	def go_home(self):
		if self.distance_y_end <= 750:
			self.time_start_y = 0.5

		# self.axis_z.motor.enable_on(False)
		self.move_home = False
		self.move(-self.distance_x_end, -self.distance_y_end - 500, -self.distance_z_end, detect = True)
		self.move_home = False
		self.move(0, -7, 0)

		self.enable_motors(False)

		self.home = True

		self.null_value()

	
	def joker_move(self):
		self.move(-300, 0, 0)
		self.move(600, 0, 0)
		self.move(-300, 0, 0)

		self.null_value()


	def move_cip(self):
		self.axis_x.motor.enable_on(False)
		self.axis_y.motor.enable_on(True)
		self.axis_z.motor.enable_on(False)

		switch_y = pins.switch_y.get_value()
		if switch_y:
			self.move(0, 870, 0)
		else:
			self.move(0, -1000, 0, detect = True)
			self.move(0, 870, 0)

		self.axis_x.motor.enable_on(False)
		self.axis_y.motor.enable_on(False)
		self.axis_z.motor.enable_on(False)


if __name__ == '__main__':
	robot = Robot_module()

	# #self.axis_z.init_go_axis(115)
	# self.axis_z.go_axis(1, 115)

	# #self.axis_z.init_go_axis(110)
	# self.axis_z.go_axis(1, 110)

	# #self.axis_z.init_go_axis(145)
	# self.axis_z.go_axis(1, 145)
     
	# #robot.go_to_point(11, 11 , 13)

	# self.axis_x.go_axis(1, 16)
	# self.axis_y.go_axis(1, 25.8)
	# self.axis_z.go_axis(1, 104)

	robot.go_to_point(-12.8, 12.8, 11)
	input()
	robot.go_home()

	robot.go_to_point(0, 16.8, 15)
	input()
	robot.go_home()
	
	robot.go_to_point(12.8, 16.8, 11)
	robot.go_home()

	robot.go_to_point(0, 16.5, 15)
	robot.go_home()

	robot.go_to_point(-12.8, 16.5, 11)
	robot.go_home()

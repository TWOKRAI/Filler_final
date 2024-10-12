import asyncio
import time

# from graphic_speed import Plotter
# from Lib.Decorators.wrapper import _timing, _log_input_output

class Motor:
	def __init__(self, name: str, pin_step, pin_direction, pin_enable):
		self.name = name

		self.stop_for = False
		
		self.pin_step = pin_step
		self.pin_direction = pin_direction
		self.pin_enable = pin_enable

		self.null_value()
		self.enable_on(False)

		self.value = 0
		self.distance = 0
		self.distance_step = 0
		self.ready = False

		self.direction = True
		
		self.speed_default = 0.00005
		self.speed_def = 0.00005
		self.speed_min = 0
		self.speed = 0
		
		self.acc_run = True
		self.acc_start = 10
		self.k = 2
		self.distance_start = 0
		self.distance_start_def = 0
		self.step_start = 0
		
		self.acc_end = 10
		self.distance_end = 0
		self.distance_end_def = 0
		self.step_end = 0

		self.limit_min = -2000
		self.limit_max = 2000
		self.error_limit = False
		self.stop = False

		self.data = []

		self.time_distance = 0

		self.step_info_1 = 0
		self.step_info_2 = 0
		self.step_info_2_2 = 0
		self.step_info_3 = 0

    
	def null_value(self):
		self.value = 0
        

	def enable_on(self, on: bool):
		if on:
			self.pin_enable.set_value(1)
		else:
			self.pin_enable.set_value(0)
    
    
	def init_acceleration(self, distance: int, mode: bool = True, print_log = False) -> float:
		if self.acc_run:
			self.speed_min = self.speed_def * self.k

			if mode: 
				self.distance_start = abs(distance) / 100 * self.acc_start
				self.distance_end = abs(distance) / 100 * self.acc_end
			else: 
				self.distance_start = self.distance_start_def
				self.distance_end = self.distance_end_def 	

			if self.distance_start != 0:
				self.step_start = abs(self.speed_min - self.speed_def) / self.distance_start

			if self.distance_end != 0:
				self.step_end = abs(self.speed_min - self.speed_def) / self.distance_end

			if print_log:
				print('init_acceleration', self.acc_start, self.acc_end, self.step_start, self.step_start, self.speed_min)

			return self.speed_min
		else:
			return self.speed_def
        

	# @_log_input_output(False)
	def acceleration(self, speed: float, step: int) -> float:
		if self.acc_run:
			if step < self.distance_start:
				speed = speed - self.step_start

			elif step >= self.distance_start and step < self.distance - self.distance_end:
				speed = self.speed_def
				
			elif step >= self.distance - self.distance_end:
				speed = speed + self.step_start
			
		return abs(speed)

	
	async def _move_async(self, distance: int, print_log = False, time_start = 0):
		self.ready = False
		self.error_limit = False

		self.distance_step = 0
		self.data = []
		
		if print_log:
			print(f'{self.name} distance: {distance}')

		self.distance = abs(round(distance, 0))

		self.speed = self.init_acceleration(self.distance)

		if distance > 0:
			direction = True
		else:
			direction = False

		if time_start > 0:
			await asyncio.sleep(time_start)

		for step in range(int(self.distance)):
			if self.stop_for:
				# print(f'{self.name}, self.stop_for')
				while self.stop_for:
					await asyncio.sleep(self.speed_def)

			
			if self.limit_min <= self.value and self.value >= self.limit_max:
				self.error_limit = True
				print(f'error limit {self.name}: {self.error_limit}')
				break
						
			if self.stop == True:
				break


			if direction == True:
				self.pin_direction.set_value(self.direction)

				self.value += 1
			else:
				self.pin_direction.set_value(not self.direction)

				self.value -= 1
				
			
			self.speed = self.acceleration(self.speed, step)


			self.pin_step.set_value(1)
			await asyncio.sleep(self.speed)

			self.pin_step.set_value(0)
			await asyncio.sleep(self.speed)

			self.data.append(self.speed)
			self.distance_step += 1 
			
			if print_log:
				print(f'{self.name} value: {self.value}, speed: {self.speed}')
				#input('&&')

		if not self.error_limit and not self.stop:
			self.ready = True

		if print_log:
			print(f'{self.name} ready: {self.ready}')


		self.stop_for = False
		self.stop = False
	

	# @_timing(True)
	async def _freq_async(self, frequency, sec, distance, accuration = True):
		self.ready = False
		self.time_distance = 0

		if distance >= 0:
			self.pin_direction.set_value(self.direction)
		else:
			self.pin_direction.set_value(not self.direction)

		if accuration == True:
			acc = False
		else:
			acc = True

		k = 0.01

		stop_distance = abs(distance) / 1000 * 0.95

		step = frequency * 1 / sec * k

		if step < 1:
			step = 1

		self.step_freq = step

		while not self.stop:
			if self.stop == True:
				break

			if acc == False:

				if step < 1: 
					step = 1

				for f in range(1, frequency, int(step)):
					if self.stop == True:
						break

					self.pin_step.frequency = f
					self.pin_step.value = 0.5
					# print(f)

					self.time_distance += k
					await asyncio.sleep(k)

					if self.time_distance >= sec:
						break

				
				acc = True

			self.time_distance += k

			self.pin_step.frequency = frequency
			self.pin_step.value = 0.5

			await asyncio.sleep(k)
						
			if self.time_distance >= stop_distance - sec:
				break
		

		for f in range(frequency, -1, -int(self.step_freq)):
			if self.stop == True:
				break

			self.pin_step.frequency = f
			self.pin_step.value = 0.5
			
			self.time_distance += k

			await asyncio.sleep(k)

			if self.time_distance >= stop_distance:	
				break
				
		self.ready = True

		self.stop_for = False
		self.pin_step.value = 0

		#print('self.time_distance', self.time_distance)


	def freq(self, frequency, k):
		asyncio.run(self._freq_async(self, frequency, k))


	async def _freq_async_new(self, steps, speed, acc_step, dec_step, start_speed, end_speed):
		if steps >= 0:
			self.pin_direction.set_value(self.direction)
		else:
			self.pin_direction.set_value(not self.direction)
		
		steps = abs(steps)

		acceleration_steps = acc_step
		deceleration_steps = dec_step

		constant_speed_steps = steps - acceleration_steps - deceleration_steps
		
		self.step_info_1 = 0
		self.step_info_2 = 0
		self.step_info_2_2 = 0
		self.step_info_3 = 0

		for i in range(acceleration_steps):
			if self.stop == True:
				break

			current_speed = start_speed + (speed - start_speed) * (i + 1) / acceleration_steps
			self.pin_step.frequency = current_speed
			self.pin_step.value = 0.5
			self.step_info_1 = i

			await asyncio.sleep(1 / current_speed)

		self.pin_step.frequency = speed
		
		for i in range(constant_speed_steps):
			if self.stop == True:
				break

			self.pin_step.value = 0.5
			self.step_info_2 = i

			await asyncio.sleep(1 / speed)
			
		for i in range(deceleration_steps):
			if self.stop == True:
				break

			current_speed = speed - (speed - end_speed) * (i + 1) / deceleration_steps
			self.pin_step.frequency = current_speed
			self.pin_step.value = 0.5
			self.step_info_3 = i

			await asyncio.sleep(1 / current_speed)		


	def freq_new(self, steps, speed, acc_step, dec_step, start_speed, end_speed):
		asyncio.run(self._freq_async_new(self, steps, speed, acc_step, dec_step, start_speed, end_speed))


	def stop_freq(self):
		self.pin_step.frequency = 0
		self.pin_step.value = 0

		self.stop = True

		#print('STOPOOOOP')


	# @_log_input_output(False)
	# @_timing(True)
	def move(self, distance: int, async_mode: bool = False, time_start = 0):
		if async_mode:
			return self._move_async(distance,  time_start = time_start)
		else:
			asyncio.run(self._move_async(distance, time_start = time_start))

	
	# async def test(self):
	# 	while not self.stop:
	# 		print(id(self.stop))

	# 		await asyncio.sleep(1)

	# 		if self.stop:
	# 			break

	
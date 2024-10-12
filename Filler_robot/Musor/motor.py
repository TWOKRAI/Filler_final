import asyncio
import gpiod
from gpiod.line import Direction, Value, Bias

#import RPI.GPIO as GPIO

import time

from Decorators.wrapper import _timing, _log_input_output


class Motor:
	def __init__(self, name: str, pin_step: int, pin_direction: int, pin_enable: int):
		self.name = name

		self.stop_for = False
		
		self.pin_step = pin_step
		self.pin_direction = pin_direction
		self.pin_enable = pin_enable


		self.chip = gpiod.Chip("/dev/gpiochip4")
		self.req = self.chip.request_lines(consumer="rpi-acloud-gpio-basic",
			config = {
				pin_step    : gpiod.LineSettings(direction=Direction.OUTPUT),
				pin_direction    : gpiod.LineSettings(direction=Direction.OUTPUT),
				pin_enable    : gpiod.LineSettings(direction=Direction.OUTPUT)
			})

		# print(dir(self.pulses_gpio))
		# self.pulse_line = self.pulses_gpio.get_line(self.pin_step)
		# self.pulse_line.request(consumer = "stepper-motor-pulses", type = gpiod.LINE_REQ_DIR_OUT)
		
		# self.pin_direction = pin_direction
		# #self.direction_gpio = gpiod.Chip('gpiochip4', gpiod.Chip.OPEN_BY_NAME)
		# self.direction_gpio = gpiod.Chip("/dev/gpiochip4")
		# self.direction_line = self.direction_gpio.get_line(self.pin_direction)
		# self.direction_line.request(consumer = "stepper-motor-direction", type = gpiod.LINE_REQ_DIR_OUT)
		
		# self.pin_enable = pin_enable
		# #self.enable_gpio = gpiod.Chip('gpiochip4', gpiod.Chip.OPEN_BY_NAME)
		# self.enable_gpio = gpiod.Chip("/dev/gpiochip4")
		# self.enable_line = self.enable_gpio.get_line(self.pin_enable)
		# self.enable_line.request(consumer = "stepper-motor-enable", type = gpiod.LINE_REQ_DIR_OUT)
		
		self.null_value()
		self.enable_on(False)

		self.value = 0
		self.distance = 0
		self.distance_step = 0
		self.ready = False

		self.direction = True
		
		self.speed_def = 0.0001
		self.speed_min = 0
		self.speed = 0
		
		self.acc_run = True
		self.acc_start = 15
		self.distance_start = 0
		self.distance_start_def = 30
		self.step_start = 0
		self.acc_end = 15
		self.distance_end = 0
		self.distance_end_def = 30
		self.step_end = 0

		self.limit_min = -2000
		self.limit_max = 2000
		self.error_limit = False
		self.stop = False

    
	def null_value(self):
		self.value = 0
        

	def enable_on(self, on: bool):
		if on:
			self.req.set_value(self.pin_enable, Value.ACTIVE)
		else:
			self.req.set_value(self.pin_enable, Value.INACTIVE)
    
    
	def init_acceleration(self, distance: int, mode: bool = True, print_log = True) -> float:
		if self.acc_run:
			self.speed_min = self.speed_def * 10

			if mode: 
				self.distance_start = abs(distance) / 100 * self.acc_start
				self.distance_end = abs(distance) / 100 * self.acc_end
			else: 
				self.distance_start = self.distance_start_def
				self.distance_end = self.distance_end_def 	

			if self.distance_start != 0 and self.distance_end != 0:
				self.step_start = abs(self.speed_min - self.speed_def) / self.distance_start
				self.step_end = abs(self.speed_min - self.speed_def) / self.distance_end

			if print_log:
				print('init_acceleration', self.acc_start, self.acc_end, self.step_start, self.step_start, self.speed_min )

			return round(self.speed_min, 6)
		else:
			return round(self.speed_def, 6)
        

	@_log_input_output(False)
	def acceleration(self, speed: float, step: int) -> float:
		if self.acc_run:
			if step < self.distance_start:
				speed = speed - self.step_start

			elif step >= self.distance_start and step < self.distance - self.distance_end:
				speed = self.speed_def
				
			elif step >= self.distance - self.distance_end:
				speed = speed + self.step_start

		return abs(round(speed, 6))

	
	async def _move_async(self, distance: int, print_log = False):
		self.ready = False
		self.error_limit = False
		
		if print_log:
			print(f'{self.name} distance: {distance}')

		self.distance = abs(round(distance, 0))

		self.speed = self.init_acceleration(self.distance)

		if distance > 0:
			direction = True
		else:
			direction = False

		for step in range(int(self.distance)):
			if self.stop_for:
				print(f'{self.name}, self.stop_for')
				while self.stop_for:
					await asyncio.sleep(self.speed_def)
			
			if self.limit_min <= self.value and self.value >= self.limit_max:
				self.error_limit = True
				print(f'error limit {self.name}: {self.error_limit}')
				break
						
			if self.stop == True:
				break

			if self.direction:
				direct1 = Value.ACTIVE
				direct2 = Value.INACTIVE
				
			else:
				direct1 = Value.INACTIVE
				direct2 = Value.ACTIVE

			if direction == True:
				self.req.set_value(self.pin_direction, direct1)
				self.value += 1
			else:
				self.req.set_value(self.pin_direction, direct2)
				self.value -= 1

			self.speed = self.acceleration(self.speed, step)

			self.req.set_value(self.pin_step, Value.ACTIVE)
			await asyncio.sleep(self.speed)

			self.req.set_value(self.pin_step, Value.INACTIVE)
			await asyncio.sleep(self.speed)

			if print_log:
				print(f'{self.name} value: {self.value}, speed: {self.speed}')
				#input('&&')

		if not self.error_limit and not self.stop:
			self.ready = True

		if print_log:
			print(f'{self.name} ready: {self.ready}')

		self.stop_for = False


	@_log_input_output(False)
	@_timing(True)
	def move(self, distance: int, async_mode: bool = False):
		if async_mode:
			return self._move_async(distance)
		else:
			asyncio.run(self._move_async(distance))


# motor_x = Motor('motor_x', 4, 3, 26)

# motor_x.move(200)
# motor_x.chip.close()
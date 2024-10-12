import gpiod
from gpiod.line import Direction, Value, Bias
import asyncio
import time

from motor import Motor
from pins_table import pins


class Motor_monitor:
    def __init__(self):
        self.pin_motor_step = 15
        self.pin_motor_dir = 21
        self.pin_motor_enable = 16

        self.pin_button = 7
        self.pin_switch_out = 8
        self.pin_switch_in = 6

        self.motor = Motor('motor-monitor', pins.motor_step, pins.motor_dir, pins.motor_enable)
        self.motor.acc_run = False
        self.motor.speed_def = 0.0001
        self.motor.limit_min = -5000
        self.motor.limit_max = 5000

        self.distance = 4500
        self.direction = False

        self.stopped = False

        # self.req.set_value(self.pin_switch_out, Value.INACTIVE)
        # self.req.set_value(self.pin_button, Value.INACTIVE)

        self.motor.enable_on(True)
        #self.req.set_value(self.pin_motor_step, Value.INACTIVE)


    def run(self):
        button = pins.get_value(pins.button)
        switch_out = pins.get_value(pins.switch_out)
        switch_in = pins.get_value(pins.switch_in)
        

        if button == True and self.direction == False:
            self.motor.enable_on(False)

            print('button')
            distance = self.distance
            asyncio.run(self._move_async(distance, detect = True))
            self.direction = not self.direction

        elif button == True and self.direction == True:
            self.motor.enable_on(False)
            print('button')
            distance = -self.distance
            asyncio.run(self._move_async(distance, detect = True))
            self.direction = not self.direction
        
        #self.motor.null_value()

    
    def mot(self):
        i = 0
        pins.set_value(pins.motor_enable, False)
        pins.set_value(pins.motor_dir, False)

        while True:
            pins.set_value(pins.motor_step, True)
            time.sleep(0.000001)

            pins.set_value(pins.motor_step, False)
            time.sleep(0.000001)

            i += 1
            print(i)


    async def _detect_sensor(self):
        i = 0
        freedom_switch = False

        while True:
            if self.motor.ready:
                break

            switch_out = pins.get_value(pins.switch_out)
            switch_in = pins.get_value(pins.switch_in)

            if switch_out == False and switch_in == False:
                i += 1
                print(i)
                if i >= 20: freedom_switch = True

            print(freedom_switch)    
            
            if (switch_out == True or switch_in == True) and freedom_switch:
                print('SWITCH')
                raise asyncio.CancelledError()
            
            if switch_out == True and self.direction == False:
                raise asyncio.CancelledError()
            
            await asyncio.sleep(0.05)


    async def _move_async(self, distance, detect = False):
        self.stopped = False
        tasks = []

        if detect:
            tasks.append(asyncio.create_task(self._detect_sensor()))

        tasks.append(asyncio.create_task(self.motor.move(distance, async_mode=True)))
            
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                if not task.done():
                    task.cancel()

        print('ready')
        self.motor.ready = False


motor_monitor = Motor_monitor()


while True:
    #motor_monitor.run()

    motor_monitor.mot()
    
    #motor_monitor.check_pin()
  
import asyncio
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import time

from Filler_robot.MotorModules.motor import Motor
from Raspberry.pins_table import pins


class Motor_monitor(QThread):
    on_signal = pyqtSignal() 
    off_signal = pyqtSignal() 
    button_signal = pyqtSignal() 


    def __init__(self):
        super().__init__()

        self.state = False

        self.motor = Motor('motor-monitor', pins.motor_step, pins.motor_dir, pins.motor_enable)

        self.motor.direction = False

        self.direct = False

        self.motor.acc_run = True
        self.motor.k = 10
        self.acc_start = 20
        self.acc_end = 20
        
        self.motor_speed = 2700
        
        self.motor.limit_min = -15000
        self.motor.limit_max = 15000
        self.distance = 6000

        self.direction = True

        self.state_button = False
        self.not_button = True

        self.motor.enable_on(True)


    def run(self):
        self.button_signal.emit()

        self.running = True 
        
        switch_out = pins.switch_out.get_value()
        switch_in = pins.switch_in.get_value()

        self.motor.enable_on(False)
        self.motor.null_value()

        if switch_in == True:
            distance = -self.distance

            self.direct = True

        elif switch_out == True:
            distance = self.distance
            self.off_signal.emit()

            self.direct = False

        elif switch_in == False and switch_out == False:
            if self.state_button:
                distance = -self.distance

                self.direct = True
            else:
                distance = self.distance

                self.direct = False
        
        asyncio.run(self._move_async(distance, detect = True))
        self.direction = not self.direction

        self.motor.enable_on(True)

    
    def down(self):
        switch_in = pins.switch_in.get_value()
        
        if switch_in == 0:
            self.motor.enable_on(False)

            distance = self.distance
            asyncio.run(self._move_async(distance, detect = True))

            self.motor.enable_on(True)
        

    async def _detect_sensor(self):
        while True:
            dir = pins.motor_dir.get_value()
            switch_out = pins.switch_out.get_value()
            switch_in = pins.switch_in.get_value()
            button = pins.button.get_value()
            button_stop = pins.button_stop.get_value()

            if not button:
                self.not_button = True

            if button and self.not_button:
                self.state_button = not self.state_button
                self.not_button = False
                raise asyncio.CancelledError()
            
            if button_stop:
                raise asyncio.CancelledError()
            
            if self.motor.ready:
                raise asyncio.CancelledError()

            if (switch_in and self.direct == False) or (switch_out and self.direct == True):
                if switch_out:
                    self.on_signal.emit()

                self.state = not self.state
                raise asyncio.CancelledError()

            await asyncio.sleep(0.01)


    async def _move_async(self, distance, detect = False):
        tasks = []

        if detect:
            tasks.append(asyncio.create_task(self._detect_sensor()))

        #tasks.append(asyncio.create_task(self.motor._freq_async(self.motor_speed, 1, distance)))
        tasks.append(asyncio.create_task(self.motor._freq_async_new(distance, 3000, 500, 500, 1, 1)))
            
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                if not task.done():
                    task.cancel()
                
        self.motor.enable_on(True)
        self.motor.ready = False


# if __name__ == '__main__':
#     motor_monitor = Motor_monitor()

#     while True:
#         motor_monitor.run()
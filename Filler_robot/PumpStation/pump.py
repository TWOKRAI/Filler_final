import asyncio
from PyQt5.QtCore import QObject, pyqtSignal

from Filler_robot.MotorModules.motor import Motor
# from Filler_robot.NeuroModules.neuron import neuron


class Pump(QObject):
    stop_pump = pyqtSignal()

    def __init__(self, name, motor_step, motor_dir, motor_enable):
        super().__init__()

        self.print_on = False

        self.name = name

        self.motor = Motor(name,  motor_step, motor_dir, motor_enable)
        self.motor.speed_def = 0.000005
        self.motor.enable_on(False)

        self.turn = 0
        self.ml = 30
        self.amount = 1
        self.step_amount = 0.0056
        self.speed = 8
        self.speed_k = 100

        self.dir = 1

        self.bottle_ml = 1000
        self.bottle_min = 100

        self.warnning = False
        self.ready_1 = False
        self.ready = False
    

    def ml_to_steps(self, ml):
        steps = 0
        if ml >= 0:
            steps = int(ml) / self.step_amount
        else:
            steps = int(ml) / self.step_amount

        if self.print_on:
            print(self.ml, self.step_amount)
            print(f'pump {self.name}, ml_to_steps // output: steps = {steps} bottle {self.bottle_ml}')

        return steps
    

    def step_to_ml(self):
        return int(self.motor.value * self.amount / self.step_amount)


    async def _pour_async(self, ml):
        self.motor.stop = False
        self.ready = False
        self.ready_1 = False
        
        self.turn = self.ml_to_steps(ml)

        speed = int(self.speed_k * self.speed)

        #print('speed', self.speed_k, speed, self.turn)

        await self.motor._freq_async_new(int(self.turn), speed, 300, 300, 100, 100)

        self.ready_1 = True
        #self.stop_pump.emit()

        await self.motor._freq_async_new(int(-600 * self.dir), speed, 300, 300, 100, 100)

        self.stop_pump.emit()
        
        self.ready = True
        

    def pour(self, ml, async_mode: bool = False):
        self.motor.stop = False
        self.ready = False

        self.motor.value = 0
        self.motor.error_limit = False
        
        if async_mode:
            return self._pour_async(ml)
        else:
            asyncio.run(self._pour_async(ml))
    

    async def _pour_async_down(self, dir):
        # self.motor.stop = False
        self.ready = False

        if dir == True:
            await self.motor._freq_async(10, 1, -500 * self.dir, accuration = False)
        else:
            await self.motor._freq_async(10, 1, -500 * self.dir, accuration = False)
    

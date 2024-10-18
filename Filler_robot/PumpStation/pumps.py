import asyncio
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import random

from Filler_robot.PumpStation.pump import Pump
from Raspberry.pins_table import pins
from Filler_interface.app import app


class Pump_station(QObject):
    minus_pump = pyqtSignal()
    bottle_1 = pyqtSignal()
    bottle_2 = pyqtSignal()
    bottles_value = pyqtSignal(int, int)
    start_pump = pyqtSignal()
    stop_pump = pyqtSignal()

    block_data_on = pyqtSignal()
    block_data_off = pyqtSignal()

    info_message = pyqtSignal(int, int)

    
    def __init__(self):
        super().__init__()

        self.connect_0 = None

        self.running = True

        self.pump_1 = Pump('pumps_1', pins.motor_p1_step, pins.motor_p1_dir, pins.motor_p1p2_enable)
        self.pump_1_enable = True
        self.pump_1.dir = -1

        self.pump_2 = Pump('pumps_2',pins.motor_p2_step, pins.motor_p2_dir, pins.motor_p1p2_enable)
        self.pump_2_enable = True
        self.pump_2.dir = 1

        self.turn1 = 0
        self.turn2 = 0

        self.filler_run = False

        self.pumping_ready = False

        self.autovalue = True
        self.cap_value = 0

        self.rullete_run = False
        self.rullete_2_run = False
        self.i_cup = 0

        # self.statistic_pump_1 = int(neuron.memory_read('memory.txt','pump_1'))
        # self.statistic_pump_2 = int(neuron.memory_read('memory.txt', 'pump_2'))
        
        self.stop = False
        self.ready = False

        self.stop_monitor = False

        self.pump_1.motor.time_distance_2 = 0 
        self.pump_2.motor.time_distance_2 = 0

        app.window_cip.power_pumps.connect(self.run)


    def run(self):
        self.enable_motors(True)

        asyncio.run(self._all_pour_async(self.pump_1.ml, self.pump_2.ml))
        # asyncio.run(self._all_pour_async(-0.3, -0.3, stop = False))
        # QThread.sleep(1)
        # asyncio.run(self._all_pour_async2())

        self.enable_motors(False)


    def filler(self):
        self.filler_run = True

        self.enable_motors(True)

        ml_1 = app.window_filler.pump_value_1 
        ml_2 = app.window_filler.pump_value_2

        self.autovalue = app.window_robot.autovalue

        #print('АВТООБЪЕМ', self.autovalue)

        if self.autovalue:
            all_ml = ml_1 + ml_2

            if all_ml > self.cap_value:
                ratio_1 = ml_1 / all_ml
                ratio_2 = ml_2 / all_ml

                ml_1 = self.cap_value * ratio_1 * 0.95
                ml_2 = self.cap_value * ratio_2 * 0.95

                #print('new_ml', ml_1, ml_2, 'ratio', ratio_1, ratio_2)

                ml_1 = int(ml_1)
                ml_2 = int(ml_2)
            
        # if self.rullete_run:
        #     ml_1, ml_2 = self.russian_rullete(ml_1, ml_2)

        # if self.rullete_2_run:
        #     ml_1, ml_2 = self.russian_rullete(ml_1, ml_2)

        if self.pumping_ready == True:
            self.info_message.emit(0, 3)
            asyncio.run(self._all_pour_async(ml_1, ml_2))
            self.info_message.emit(0, 4)
        else:
            self.info_message.emit(1, 3)
            self.bottles_value.emit(30, 30)
            asyncio.run(self._all_pour_async(30, 30))
            self.pumping_ready = True
            self.info_message.emit(0, 1)

        self.enable_motors(False)

        #self.stop_pump.emit()


    def russian_rullete(self, ml_1, ml_2):
        ratio_1 = random.random()
        
        all_value = (ml_1 + ml_2)

        if self.autovalue:
            if self.cap_value <= all_value:
                all_value = self.cap_value

        if ml_1 != 0:
            ml_1 = all_value * ratio_1 * 0.95
        else:
            ml_1 = 0

        if ml_2 != 0:
            ml_2 = all_value * (1 - ratio_1) * 0.95
        else:
            ml_2 = 0

        #print('RUSSIAN RULLETE', ml_1, ml_2)

        return ml_1, ml_2


    def prepare(self):
        self.filler_run = False
        self.enable_motors(True)
        
        asyncio.run(self._all_pour_async(30, 30))

        self.enable_motors(False)


    def cip(self):
        self.filler_run = False

        self.enable_motors(True)

        asyncio.run(self._all_pour_async(1000, 1000))

        self.enable_motors(False)

    
    def enable_motors(self, value = False):
        self.pump_1.motor.enable_on(value)
        self.pump_2.motor.enable_on(value)

    
    def stop_pumps(self):
        self.stop2 = True
        self.stop_monitor = True

        self.pump_1.motor.stop = True
        self.pump_2.motor.stop = True

        self.enable_motors(False)


    async def _stop_pumps(self):
        self.pump_1.motor.time_distance_2 = 1
        self.pump_2.motor.time_distance_2 = 1

        while not self.stop2:
            if pins.button_stop.get_value():
                self.stop_pumps()
            
            await asyncio.sleep(0.05)

            if self.stop2 == True or (self.pump_1.ready == True and self.pump_2.ready == True):
                self.pump_1.motor.stop = True
                self.pump_2.motor.stop = True

                self.stop_monitor = True

                # self.minus_pump.emit()

                raise asyncio.CancelledError()
            
            await asyncio.sleep(0.05)


    async def _monitor_filler(self):
        while not self.stop_monitor:
            if not self.pump_1.ready_1:
                value1 = self.turn1 - self.pump_1.motor.step_info_2 * self.pump_1.step_amount
                value1 = int(round(value1, 0))
            else:
                value1 = 0

            await asyncio.sleep(0.05)

            if not self.pump_2.ready_1:
                value2 = self.turn2 - self.pump_2.motor.step_info_2 * self.pump_2.step_amount
                value2 = int(round(value2, 0))
            else:
                value2 = 0

            await asyncio.sleep(0.05)
            
            if not self.pump_1.ready_1 or not self.pump_2.ready_1:
                self.bottles_value.emit(value1, value2)
            else:
                self.bottles_value.emit(0, 0)
            
            await asyncio.sleep(0.1)

    
    # async def _pour_async2(self, motor, turn):
    #     await motor._freq_async2(1000, 1, turn)


    async def _all_pour_async(self, turn1, turn2, stop = True):
        self.start_pump.emit()
        self.block_data_on.emit()

        self.turn1 = turn1
        self.turn2 = turn2

        # print( ' self.pump_1.motor.stop', self.pump_1.motor.stop,  self.pump_2.motor.stop)
        # print( ' turn1, turn2', turn1,  turn2)

        self.stop2 = False
        self.stop_monitor = False

        self.pump_1.ready = False
        self.pump_2.ready = False

        tasks = []

        if stop == True:
            tasks.append(asyncio.create_task(self._stop_pumps()))

        # tasks.append(asyncio.create_task(self.pump_1.motor.test()))

        if turn1 != 0 and self.pump_1_enable:
            tasks.append(asyncio.create_task(self.pump_1._pour_async(-turn1)))
        else:
            self.pump_1.ready = True
         
        if turn2 != 0 and self.pump_2_enable:
            tasks.append(asyncio.create_task(self.pump_2._pour_async(turn2)))
        else:
            self.pump_2.ready = True

        tasks.append(asyncio.create_task(self._monitor_filler()))

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                if not task.done():
                    task.cancel()
        
        
        self.stop_pump.emit()
        self.block_data_off.emit()
        
    
    async def _all_pour_async2(self):
        #print('START DOWN')

        self.stop2 = False
        self.pump_1.ready = False
        self.pump_2.ready = False

        tasks = []

        tasks.append(asyncio.create_task(self.pump_1._pour_async_down(True)))
        tasks.append(asyncio.create_task(self.pump_2._pour_async_down(True)))

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                if not task.done():
                    task.cancel()
        
    
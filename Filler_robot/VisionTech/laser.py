from Raspberry.pins_table import pins
from PyQt5.QtCore import QThread
		
from Filler_interface.app import app


class Laser:
    def __init__(self) -> None:
        self.connect_0 = None

        self.mode = 2
        self.laser_on = False

        self.first = False

        self.freq = 100
        self.coll = 30
        self.step = 7


    def running(self):
        self.mode = app.window_robot.laser_mode

        match self.mode:
            case 0:
                if self.first:
                    self.on_off(1)
                    QThread.msleep(2100)
        
                self.on_off(0)
            case 1:
                self.on_off(1)
            case 2:
                self.freq_func(self.freq, self.coll, self.step)
            case _:
                self.on_off(0)

        self.first = True
        

    def on_off(self, value):
        self.mode = app.window_robot.laser_mode
    
        if  self.mode != 0:
            pins.laser.set_value(value)
        else:
            pins.laser.set_value(0)

    
    def freq_func(self, frequ, coll, step):
        for _ in range(coll):
            QThread.msleep(frequ)
            pins.laser.set_value(1)
            
            QThread.msleep(frequ)
            pins.laser.set_value(0)

            frequ -= step 

            if frequ <= 0:
                frequ = 1
        
        self.on_off(0)

    
    def first_start(self):
        self.freq_func(100, 40, self.step)




from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject

from Filler_robot.VisionTech.camera import Camera
from Filler_robot.NeuroModules.neuron import Neuron
from Filler_robot.NeuroModules.interface import Interface
from Filler_robot.PumpStation.pumps import Pump_station
from Filler_robot.Robots.robot_module import Robot_module
from Filler_robot.VisionTech.laser import Laser

from Raspberry.Temperature import check_temperature, write_to_file, clear_file

from Filler_interface import app


class Robot_filler(QThread):
    prepare = pyqtSignal()
    start_state = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()

        self.running = False

        self.laser = Laser() 
        self.laser.on_off(1)

        self.camera = Camera()

        self.neuron = Neuron(self.camera)
    
        self.interface = Interface(self.camera, self.neuron)
        self.neuron.interface = self.interface

        self.pump_station = Pump_station()

        self.robot = Robot_module(self.camera, self.neuron, self.interface, self.pump_station, self.laser)

        self.filler = False
        self.calibration_func = False
        self.view = False
        self.cip = False
        self.cip_move = False
        self.calibration_only = False
        self.calibration_first = False

        self.first_view = False

        self.button_error = False 
        
        clear_file('log_temp.txt')

        self.i = 0
        self.time = 0

        #self.robot.motor_z.enable_on(True)

        self.first = False

        self.pumping_ready = False


    def stop(self):
        self.running = False
        print('stop thread Robot')
    

    def run(self) -> None:
        print('stop thread Robot')

        self.running = True
        self.robot.pumping_find = False
        self.robot.find = False

        i = 0

        QThread.msleep(1000)

        while self.running:  
            # print(i)
            # i += 1

            self.view_run2()
            self.filler_run2()
            self.calibration_run2()
            self.cip_run2()
            self.calibration_only_run2()
            self.calibration_first_run2()
            self.cip_move_run2()

            if not self.filler and not self.view:
                self.laser.on_off(0)

            if self.filler:
                self.time += 1
            else:
                self.time += 0.1

            if self.time > 100:
                self.robot.enable_motors(False)
                self.pump_station.enable_motors(False)

                temp = check_temperature()
                write_to_file(temp, 'log_temp.txt')

                print('OFF TIMER')

                self.robot.calibration_ready = False 

                self.time = 0
                
            QThread.msleep(100)

        self.camera.stop()

        print('Out thread robot')


    def starting(self):
        self.calibration_first_run()

    
    def all_stop(self):
        self.view = False
        self.filler = False
        self.calibratiom_func = False
        self.cip = False
        self.cip_move = False


    def view_run(self):
        self.view = True
        self.filler = False
        self.calibratiom_func = False
        self.cip = False
        self.cip_move = False


    def view_run2(self):
        while self.view:
            print('view run')
            self.laser.on_off(0)
            self.robot.enable_motors(False)

            if not self.first_view:
                self.camera.running()
                self.neuron.find_objects()
                self.interface.running()
                self.first_view = True

            self.camera.running()
            self.neuron.neuron_vision()

            self.interface.running()

            QThread.msleep(500)
    

    def view_stop(self):
        self.view = False
        self.first_view = False


    def filler_run(self):
        self.view = False
        self.filler = True
        self.calibration_func = False
        self.cip = False
        self.cip_move = False

        self.time = 0

        self.robot.start = True


    def filler_run2(self):
        while self.filler:
            if not self.filler: break

            self.start_state.emit(1)

            print('filler run')

            self.laser.on_off(1)

            QThread.msleep(1000)

            if not self.filler: break
            self.camera.running()

            if not self.filler: break
            find_tuple = self.neuron.find_objects()

            if find_tuple[1] > 0:
                if self.robot.calibration_ready == False:
                    self.robot.calibration()

                self.laser.running()
                self.laser.on_off(0)
                
                self.camera.running()

                if not self.filler: break
                self.neuron.neuron_vision()

                self.time = 0

            self.interface.running()
            
            if not self.filler: break
            self.robot.running()
        
        self.start_state.emit(0)


    def filler_stop(self):
        self.filler = False

        self.robot.start = False


    def calibration_run(self):
        self.view = False
        self.filler = False
        self.calibration_func = True
        self.cip = False
        self.cip_move = False

        self.time = 0


    def calibration_run2(self):
        if self.calibration_func:
            print('calibration_func run')

            if not self.button_error: self.robot.calibration()
            
            if not self.button_error: self.prepare.emit()

            if not self.button_error: self.pumping()

            self.calibratiom_func = False


    def calibration_stop(self):
        self.calibration_func = False

    
    def cip_run(self):
        self.view = False
        self.filler = False
        self.calibration_func = False
        self.cip = True
        self.cip_move = False

    
    def cip_run2(self):
        if self.cip:
            print('cip run')

            self.pump_station.cip()
            self.cip_stop()


    def cip_stop(self):
        self.cip = False


    def cip_move_run(self):
        self.view = False
        self.filler = False
        self.calibration_func = False
        self.cip = False
        self.cip_move = True


    def cip_move_run2(self):
        if self.cip_move:
            print('cip_move run')

            self.robot.move_cip()

            self.cip_move_stop()



    def cip_move_stop(self):
        self.cip_move = False


    def calibration_only_run(self):
        self.view = False
        self.filler = False
        self.calibration_func = False
        self.cip = False
        self.cip_move = False
        self.calibration_only = True


    def calibration_only_run2(self):
        if self.calibration_only:
            print('calibration run')

            self.robot.calibration()

            self.calibration_only = False


    def calibration_first_run(self):
        self.calibration_first = True


    def calibration_first_run2(self):
        if self.calibration_first:
            if self.first == False:
                self.robot.calibration()
                self.calibration_only = False

                self.laser.first_start()

            self.first = True


    def reset_calibration(self):
        self.calibration_stop()
        self.robot.calibration_ready = False

        # self.robot.pumping_find = False
        self.robot.find = False

        self.pumping_ready = False

        self.robot.no_stop_motors()

        self.neuron.forget()

        # self.robot.enable_motors(False)



    def pumping(self):
        self.robot.pumping_find = True
        self.robot.find = False
        
        self.robot_on = True

        while not self.robot.find and self.calibration_func and not self.button_error:
            self.laser.on_off(1)
            
            self.camera.running()
            find_tuple = self.neuron.find_objects()
    
            if find_tuple[1] > 0:
                self.laser.running()
                self.laser.on_off(0)

                self.camera.running()
                self.neuron.neuron_vision()

            if self.robot_on: self.robot.running()

            if self.robot.find:
                self.robot.find = False
                break

            QThread.msleep(100)
            
            print(' Не нашел')
        
        print('нашел')

        if self.calibration_func:
            if not self.button_error: self.prepare.emit()

            if not self.button_error: self.pump_station.prepare()

            if not self.button_error: self.prepare.emit()
            self.robot.go_home()
        
            if not self.button_error: self.prepare.emit()

            self.robot.pumping_find = False
            self.robot.find = False

            self.pumping_ready = True


    def stop_pumping(self):
        self.robot.pump_station.stop_pumps2()


    def on_button_error(self):
        self.button_error = True
        self.robot.enable_motors(True)


    def no_button_error(self):
        self.robot.no_stop_motors()

        self.button_error = False

    
    def error_button(self):
        self.button_error = True
        self.robot.button_stop = True

        self.all_stop()

        self.filler_stop()
        self.robot.stop_motors()
        self.pump_station.stop_pumps()
        self.robot.enable_motors(True)

        self.pumping_ready = False
        self.robot.calibration_ready = False
        #self.reset_calibration()
        self.neuron.forget()

    
    def no_error_button(self):
        self.button_error = False
        self.robot.button_stop = False
        

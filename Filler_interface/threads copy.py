from PyQt5.QtCore import QThread, pyqtSignal

from robot_main import Robot_filler
from Filler_robot.PumpStation.pumps import Pump_station

from Threads.input import Input_request


from Filler_interface.app import app
from Filler_interface.filler import filler


class Thread():
    def __init__(self):
        self.input_request = Input_request()

        self.robot_filler = Robot_filler()

        # self.thread_robot = QThread()
        # self.robot_filler = None

        self.thread_pumps = QThread()
        self.pumps = None



    def start_view_thread(self, camera_on = False, neuron_on = False, interface_on = False, robot_on = False):
        if not self.thread_robot.isRunning():
            self.thread_robot = QThread()
            self.robot_filler = Robot_filler(camera_on = camera_on, neuron_on = neuron_on, interface_on = interface_on, robot_on = robot_on)
            self.robot_filler.moveToThread(self.thread_robot)

            if app.ready == True:
                self.robot_filler.robot.calibration_ready = True
                self.robot_filler.robot.pumping_find = False

                self.thread_robot.started.connect(self.robot_filler.run)

                self.robot_filler.interface.frame_captured.connect(app.window_view.update_frame)
                # self.input_request.error.connect(self.robot_filler.robot.stop_motors)

                # app.window_prepare.calibration.connect(self.robot_filler.calibration)
                # app.window_prepare.reset_calibration.connect(self.robot_filler.reset_calibration)
                # app.window_prepare.find_cup.connect(self.robot_filler.find_cup)
                # app.window_prepare.pumping.connect(self.robot_filler.pumping)
                # app.window_prepare.stop_pumping.connect(self.robot_filler.robot.pump_station.stop_pumps2)

                # self.robot_filler.robot.prepare.connect(app.window_prepare.update_prepare)

            self.thread_robot.start()


    def start_filler_thread(self, camera_on = False, neuron_on = False, interface_on = False, robot_on = False):
        if not self.thread_robot.isRunning():
            self.thread_robot = QThread()
            self.robot_filler = Robot_filler(camera_on = camera_on, neuron_on = neuron_on, interface_on = interface_on, robot_on = robot_on)
            self.robot_filler.moveToThread(self.thread_robot)

            if app.ready == True:
                self.robot_filler.robot.calibration_ready = True
                self.robot_filler.robot.pumping_find = False
                
                self.robot_filler.robot.pump_station.pump_1.bottle_ml = filler.param3
                self.robot_filler.robot.pump_station.pump_2.bottle_ml = filler.param4
                self.robot_filler.robot.pump_station.pump_1.ml = filler.param5
                self.robot_filler.robot.pump_station.pump_2.ml = filler.param6

                self.robot_filler.robot.pump_station.bottle_1.connect(app.window_filler.update_bottle_1)
                self.robot_filler.robot.pump_station.bottle_2.connect(app.window_filler.update_bottle_2)

                self.thread_robot.started.connect(self.robot_filler.run)

                self.robot_filler.interface.frame_captured.connect(app.window_view.update_frame)
                # self.input_request.error.connect(self.robot_filler.robot.stop_motors)

                # app.window_prepare.calibration.connect(self.robot_filler.calibration)
                # app.window_prepare.reset_calibration.connect(self.robot_filler.reset_calibration)
                # app.window_prepare.find_cup.connect(self.robot_filler.find_cup)
                # app.window_prepare.pumping.connect(self.robot_filler.pumping)
                # app.window_prepare.stop_pumping.connect(self.robot_filler.robot.pump_station.stop_pumps2)
                # # app.window_prepare.start_filler.connect(self.robot_filler.run2)
                
                # self.robot_filler.robot.prepare.connect(app.window_prepare.update_prepare)

            self.thread_robot.start()
        

    # def put_pumps(self):
    #     print('filler.paramm5', filler.paramm5, 'filler.paramm6', filler.paramm6)
    #     self.robot_filler.robot.pump_station.pump_1.ml = filler.paramm5
    #     self.robot_filler.robot.pump_station.pump_2.ml = filler.paramm6


    def start_robot_thread(self, camera_on = False, neuron_on = False, interface_on = False, robot_on = False):
        if not self.thread_robot.isRunning():
            self.thread_robot = QThread()
            self.robot_filler = Robot_filler(camera_on = camera_on, neuron_on = neuron_on, interface_on = interface_on, robot_on = robot_on)
            self.robot_filler.moveToThread(self.thread_robot)

            if app.ready == True:
                self.robot_filler.robot.calibration_ready = False
                self.robot_filler.robot.pumping_find = False

                # self.thread_robot.started.connect(self.robot_filler.run)

                self.robot_filler.interface.frame_captured.connect(app.window_view.update_frame)
                self.input_request.error.connect(self.robot_filler.robot.stop_motors)

                app.window_prepare.calibration.connect(self.robot_filler.calibration)
                app.window_prepare.reset_calibration.connect(self.robot_filler.reset_calibration)
                app.window_prepare.find_cup.connect(self.robot_filler.find_cup)
                app.window_prepare.pumping.connect(self.robot_filler.pumping)
                app.window_prepare.stop_pumping.connect(self.robot_filler.robot.pump_station.stop_pumps2)
                # app.window_prepare.start_filler.connect(self.robot_filler.run2)
                
                self.robot_filler.robot.prepare.connect(app.window_prepare.update_prepare)

            self.thread_robot.start()
    

    def stop_robot_thread(self):
        if self.thread_robot is not None and self.thread_robot.isRunning():
            self.robot_filler.stop()
            self.thread_robot.quit()
            self.thread_robot.wait()
            # self.thread_robot = None
            # self.robot_filler = None
    

    def start_calibration(self):
        if self.thread_robot.isRunning():
            self.thread_robot.quit()
            self.thread_robot.wait()
    
        self.thread_robot.started.connect(self.robot_filler.calibration)
        self.thread_robot.start()

    
    def find_cup(self):
        if self.thread_robot.isRunning():
            self.thread_robot.quit()
            self.thread_robot.wait()
    
        self.thread_robot.started.connect(self.robot_filler.find_cup)
        self.thread_robot.start()


    def pumping(self):
        self.start_pumps_thread(self, True, True, 900, 900)


    def start_robot_thread(self):
        self.robot_filler.camera_on = True
        self.robot_filler.neuron_on = True 
        self.robot_filler.interface_on = True

        if not self.robot_filler.isRunning():
            if app.ready == True:
                self.robot_filler.interface.frame_captured.connect(app.window_view.update_frame)
                self.input_request.error.connect(self.robot_filler.robot.stop_motors)

                app.window_prepare.calibration.connect(self.robot_filler.calibration)
                app.window_prepare.reset_calibration.connect(self.robot_filler.reset_calibration)
                app.window_prepare.find_cup.connect(self.robot_filler.find_cup)
                app.window_prepare.pumping.connect(self.robot_filler.pumping)
                app.window_prepare.stop_pumping.connect(self.robot_filler.robot.pump_station.stop_pumps2)
                # app.window_prepare.start_filler.connect(self.robot_filler.run2)
                
                self.robot_filler.robot.prepare.connect(app.window_prepare.update_prepare)

            self.robot_filler.start()


    def stop_robot_thread(self):
        self.robot_filler.stop()


    def start_input_thread(self):
        if not self.input_request.isRunning():
            if app.ready == True:
                self.input_request.show_error.connect(app.window_error.show)
                self.input_request.error.connect(self.stop_robot_thread)
                self.input_request.error.connect(self.stop_pumps_thread)
                self.input_request.error.connect(self.robot_filler.robot.stop_motors)
                
                self.input_request.close_error.connect(app.window_error.close)

                self.input_request.motor_monitor.on_signal.connect(app.window_start.close)
                self.input_request.motor_monitor.button_signal.connect(app.window_start.show)
                self.input_request.motor_monitor.off_signal.connect(app.window_start.show)
                self.input_request.motor_monitor.off_signal.connect(app.window_view.close)
                # self.input_request.motor_monitor.off_signal.connect(self.stop_input_thread)

                self.input_request.error.connect(app.window_view.close)

            self.input_request.start()


    def stop_input_thread(self):
        self.input_request.stop()


    def start_pumps_thread(self, pump1, pump2, speed_1, speed_2):
        if not self.thread_pumps.isRunning():
            self.thread_pumps = QThread()
            self.pumps = Pump_station()

            self.pumps.pump_1_enable = pump1
            self.pumps.pump_1.speed = speed_1

            self.pumps.pump_2_enable = pump2
            self.pumps.pump_2.speed = speed_2

            self.pumps.moveToThread(self.thread_pumps)
            self.thread_pumps.started.connect(self.pumps.run)

            if app.ready == True:
                app.window_cip.stop_pumps_signal.connect(self.stop)
                self.input_request.error.connect(self.stop)
                self.input_request.error.connect(self.stop_pumps_thread)

                self.pumps.minus_pump.connect(app.window_cip.close)
                
            self.thread_pumps.start()


    def stop(self):
        self.pumps.stop_pumps2()
    

    def stop_pumps_thread(self):
        self.thread_pumps.quit()
        self.thread_pumps.wait()

            # self.thread_robot = None
            # self.robot_filler = None


    # def start_monitor_thread(self):
    #     if not self.thread_robot.isRunning():
    #         self.thread_monitor = QThread()
    #         self.motor_monitor = Motor_monitor()
    #         self.motor_monitor.moveToThread(self.thread_monitor)
    #         self.thread_monitor.started.connect(self.motor_monitor.run)

    #         if app.ready == True:
    #             self.motor_monitor.show_error.connect(app.window_error.show)
    #             self.motor_monitor.error.connect(self.stop_robot_thread)
    #             self.motor_monitor.close_error.connect(app.window_error.close)

    #             self.motor_monitor.motor_monitor.on_signal.connect(app.window_start.close)

    #             self.motor_monitor.motor_monitor.off_signal.connect(app.window_start.show)
    #             self.motor_monitor.motor_monitor.off_signal.connect(app.window_view.close)
    #             self.motor_monitor.motor_monitor.off_signal.connect(self.stop_monitor_thread)

    #         self.thread_input.start()
    

    # def stop_monitor_thread(self):
    #     if self.thread_robot is not None and self.thread_robot.isRunning():
    #         self.motor_monitor.stop()
    #         self.thread_input.quit()
    #         self.thread_input.wait()
    #         # self.thread_robot = None
    #         # self.robot_filler = None


# thread = Thread()
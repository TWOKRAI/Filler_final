from Threads.robot_main import Robot_filler
from Threads.input import Input_request

from Filler_interface.app import app


class Thread():
    def __init__(self):
        self.input_request = Input_request()
        self.robot_filler = Robot_filler()

        self.connects()
        
        self.start_input_thread()
        self.start_robot_thread()

    
    def connects(self):
        self.connect_app_thread()
        self.connect_input_thread()
        self.connect_robot_thread()
        
    
    def connect_app_thread(self):
        app.window_filler.start_filler.connect(self.input_request.block_button_on)
        app.window_filler.stop_filler.connect(self.input_request.block_button_off)
        app.window_filler.start_filler.connect(self.robot_filler.filler_run)
        app.window_filler.stop_filler.connect(self.robot_filler.pump_station.stop_pumps)
        app.window_filler.stop_filler.connect(self.robot_filler.filler_stop)
        
        app.window_cip.stop_pumps_signal.connect(self.robot_filler.pump_station.stop_pumps)

        # app.window_prepare.calibration.connect(self.robot_filler.calibration)
        app.window_prepare.reset_calibration.connect(self.robot_filler.reset_calibration)
        app.window_prepare.pumping.connect(self.robot_filler.pumping)

        app.button_start.connect(self.robot_filler.filler_run)
        app.button_stop.connect(self.robot_filler.pump_station.stop_pumps)
        app.button_stop.connect(self.robot_filler.filler_stop)

        app.button_calibration.connect(self.robot_filler.calibration_only_run)
        app.button_motor.connect(self.robot_filler.enable_on_off)

        # app.window_filler.stop_filler.connect(self.robot_filler.robot.stop_motors)
        # app.window_filler.stop_filler.connect(self.robot_filler.neuron.forget)

        app.window_view.view_start.connect(self.robot_filler.view_run)
        app.window_view.view_stop.connect(self.robot_filler.view_stop)


    def connect_input_thread(self):
        if app.ready == True:
            self.input_request.starting.connect(self.robot_filler.starting)

            self.input_request.button_monitor.connect(self.robot_filler.all_stop)

            self.input_request.show_error.connect(app.window_error.show)
            # self.input_request.error.connect(self.stop_robot_thread)
            # self.input_request.error.connect(self.stop_pumps_thread)
            # self.input_request.error.connect(self.robot_filler.robot.stop_motors)
            # self.input_request.no_error.connect(app.window_prepare.reset)
            # self.input_request.no_error.connect(self.robot_filler.robot.no_stop_motors)
            
            self.input_request.error.connect(self.robot_filler.error_button)
            # self.input_request.error.connect(self.robot_filler.robot.stop_motors)
            # self.input_request.error.connect(self.robot_filler.pump_station.stop_pumps)
            # self.input_request.error.connect(self.robot_filler.reset_calibration)
            # self.input_request.error.connect(self.robot_filler.filler_stop)
            # self.input_request.error.connect(self.robot_filler.on_button_error)
            
            
            self.input_request.no_error.connect(app.window_prepare.reset)
            self.input_request.no_error.connect(self.robot_filler.no_error_button)
            self.input_request.no_error.connect(app.window_main_filler.show)

            self.input_request.close_error.connect(app.window_error.close)

            self.input_request.motor_monitor.on_signal.connect(app.window_start.close)
            self.input_request.motor_monitor.button_signal.connect(app.window_start.show)
            self.input_request.motor_monitor.off_signal.connect(app.window_start.show)
            self.input_request.motor_monitor.off_signal.connect(app.window_view.close)
            # \\self.input_request.motor_monitor.off_signal.connect(self.stop_input_thread)


            # app.window_filler.start_filler.connect(self.input_request.block_button_on)
            # app.window_filler.stop_filler.connect(self.input_request.block_button_off)

            self.input_request.motor_monitor.button_signal.connect(self.robot_filler.pump_station.stop_pumps)
            self.input_request.motor_monitor.button_signal.connect(self.robot_filler.filler_stop)
            self.input_request.motor_monitor.button_signal.connect(app.window_prepare.reset)
            #self.input_request.motor_monitor.button_signal.connect(self.robot_filler.calibration_only_run)

            self.input_request.error.connect(app.window_view.close)

            # app.window_cip.stop_pumps_signal.connect(self.robot_filler.pump_station.stop_pumps)

    
    def start_input_thread(self):
        if not self.input_request.isRunning():
            if self.input_request == None:
                self.input_request = Input_request()

            self.connect_input_thread()
            self.input_request.start()


    def stop_input_thread(self):
        if self.input_request != None:
            self.input_request.stop()
        
        self.input_request = None


    def connect_robot_thread(self):
        if app.ready == True:
            self.robot_filler.interface.frame_captured.connect(app.window_view.update_frame)

            # # app.window_prepare.calibration.connect(self.robot_filler.calibration)
            # app.window_prepare.reset_calibration.connect(self.robot_filler.reset_calibration)
            # app.window_prepare.pumping.connect(self.robot_filler.pumping)

            # app.window_filler.start_filler.connect(self.robot_filler.filler_run)
            # app.window_filler.stop_filler.connect(self.robot_filler.pump_station.stop_pumps)
            # app.window_filler.stop_filler.connect(self.robot_filler.filler_stop)
            
            # app.button_start.connect(self.robot_filler.filler_run)
            # app.button_stop.connect(self.robot_filler.pump_station.stop_pumps)
            # app.button_stop.connect(self.robot_filler.filler_stop)

            # app.button_calibration.connect(self.robot_filler.calibration_only_run)
            # app.button_motor.connect(self.robot_filler.enable_on_off)

            # # app.window_filler.stop_filler.connect(self.robot_filler.robot.stop_motors)
            # # app.window_filler.stop_filler.connect(self.robot_filler.neuron.forget)

            # app.window_view.view_start.connect(self.robot_filler.view_run)
            # app.window_view.view_stop.connect(self.robot_filler.view_stop)

            #self.robot_filler.pump_station.bottle_1.connect(app.window_filler.value_update_pump_1)
            #self.robot_filler.pump_station.bottle_2.connect(app.window_filler.value_update_pump_2)
            self.robot_filler.pump_station.bottles_value.connect(app.window_filler.value_update_pumps)

            self.robot_filler.pump_station.start_pump.connect(app.window_filler.start_pump)
            self.robot_filler.pump_station.stop_pump.connect(app.window_filler.stop_pump)

            # self.robot_filler.pump_station.pump_1.stop_pump.connect(app.window_filler.stop_pump_1)
            # self.robot_filler.pump_station.pump_2.stop_pump.connect(app.window_filler.stop_pump_2)

            # app.window_prepare.stop_pumping.connect(self.robot_filler.robot.pump_station.stop_pumps2)
            # app.window_prepare.start_filler.connect(self.robot_filler.run2)
            
            self.robot_filler.prepare.connect(app.window_prepare.button_calibr_clicked)

            self.robot_filler.start_state.connect(app.window_filler.button_start_update)

            self.robot_filler.robot.block_data_on.connect(app.block_on)
            self.robot_filler.robot.block_data_off.connect(app.block_off)

            self.robot_filler.pump_station.block_data_on.connect(app.block_on)
            self.robot_filler.pump_station.block_data_off.connect(app.block_off)


    def start_robot_thread(self):
        if not self.robot_filler.isRunning():
            if self.robot_filler == None:
                self.robot_filler = Robot_filler()

            self.connect_robot_thread()
            self.robot_filler.start()


    def stop_robot_thread(self):
        if self.robot_filler != None:
            self.robot_filler.stop()
        
        #self.robot_filler = None
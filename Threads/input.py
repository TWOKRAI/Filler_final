from PyQt5.QtCore import QThread, pyqtSignal

from Raspberry.pins_table import pins

from Filler_robot.Monitor.motor_monitor import Motor_monitor

from Filler_interface.app import app


class Input_request(QThread):
    error = pyqtSignal()
    no_error = pyqtSignal()

    show_error = pyqtSignal()
    close_error = pyqtSignal()

    starting = pyqtSignal()

    start_show = pyqtSignal()
    view_close = pyqtSignal()
    filler_stop = pyqtSignal()
    

    button_monitor = pyqtSignal()


    def __init__(self) -> None:
        super().__init__()

        self.running = True

        self.connect_0 = None

        self.run_request = True
        self.time_request = 50

        self.button_error = False

        self.motor_monitor = Motor_monitor()

        self.button = False
        self.first = False

        self.block = False

        self.monitor_run = False


    def run(self):
        self.running = True
    
        self.request()


    def stop(self):
        self.running = False


    def request(self):
        while self.running:
            if not self.first:
                self.motor_monitor.down()
                self.first = True

          
            if pins.button_stop.get_value():
                self.show_error.emit()

                # if self.button_error == False:
                self.error.emit()

                self.button_error = True
            else:
                if self.button_error == True:
                    self.close_error.emit()
                    self.no_error.emit()

                self.button_error = False
            
            if pins.button.get_value():
                if not self.block:
                    self.motor_start()
                    # self.button_monitor.emit()
                    # #self.starting.emit()

                    # self.motor_monitor.start()

            
            if self.monitor_run == True:
                if not self.block: 
                    self.motor_monitor.start()
                
                self.monitor_run = False


            QThread.msleep(int(self.time_request))


    def connect(self):
        self.starting.connect(self.connect_0.robot_filler.starting)

        self.button_monitor.connect(self.connect_0.robot_filler.all_stop)

        self.show_error.connect(app.window_error.show)
      
        self.error.connect(self.connect_0.robot_filler.error_button)
 
        self.no_error.connect(app.window_prepare.reset)
        self.no_error.connect(self.connect_0.robot_filler.no_error_button)
        self.no_error.connect(app.window_main_filler.show)

        self.close_error.connect(app.window_error.close)


        self.start_show.connect(app.window_start.show)
        self.view_close.connect(app.window_view.close)

        self.filler_stop.connect(self.connect_0.robot_filler.pump_station.stop_pumps)
        self.filler_stop.connect(self.connect_0.robot_filler.filler_stop)
        

        # self.motor_monitor.on_signal.connect(app.window_start.close)
        # self.motor_monitor.button_signal.connect(app.window_start.show)
        # self.motor_monitor.off_signal.connect(self.motor_off_signal)

        # self.motor_monitor.button_signal.connect(self.connect_0.robot_filler.pump_station.stop_pumps)
        # self.motor_monitor.button_signal.connect(self.connect_0.robot_filler.filler_stop)
        # self.motor_monitor.button_signal.connect(app.window_prepare.reset)
 
        self.error.connect(app.window_view.close)


    def block_button_on(self):
        self.block = True
    

    def block_button_off(self):
        self.block = False

    
    def motor_start(self):
        self.filler_stop.emit()
        QThread.msleep(200)
        self.start_show.emit()
        QThread.msleep(100)
        self.view_close.emit()
        
        if not self.motor_monitor.isRunning():
            QThread.msleep(100)
            self.motor_monitor.start()
        

# input_request = Input_request()
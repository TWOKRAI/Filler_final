from PyQt5.QtCore import QThread, pyqtSignal

from Raspberry.pins_table import pins

from Filler_robot.Monitor.motor_monitor import Motor_monitor


class Input_request(QThread):
    pin_values_updated = pyqtSignal(dict)
    show_error = pyqtSignal()
    close_error = pyqtSignal()
    error = pyqtSignal()
    no_error = pyqtSignal()

    starting = pyqtSignal()

    button_monitor = pyqtSignal()


    def __init__(self) -> None:
        super().__init__()
        self.running = True

        self.run_request = True
        self.time_request = 100

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

            try:
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
                        self.button_monitor.emit()
                        self.starting.emit()

                        self.motor_monitor.start()

                        #self.time_request = 200

                
                if self.monitor_run == True:
                    if not self.block: 
                        self.motor_monitor.start()
                   
                    self.monitor_run = False
                    
                    # QThread.msleep(100)

        
            except Exception as e:
                print(f"Error reading pin values: {e}")

            QThread.msleep(int(self.time_request))


    def block_button_on(self):
        self.block = True
    

    def block_button_off(self):
        self.block = False


# input_request = Input_request()
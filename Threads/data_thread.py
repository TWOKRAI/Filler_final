from PyQt5.QtCore import QThread, pyqtSignal

#from Server.database import DatabaseManager
from Server.database_postgresql import DatabaseManager

from Filler_interface.app import app


class Data_request(QThread):
    update = pyqtSignal(dict)
    button_start = pyqtSignal()
    button_stop = pyqtSignal()


    def __init__(self) -> None:
        super().__init__()
        self.running = False

        self.block = False

        self.run_request = True
        self.time_request = 1000

        self.data = None
        self.data_prev = None

        #self.database = DatabaseManager('Server/myproject/db.sqlite3')

        self.database = DatabaseManager(
            db_name='myapp',
            db_user='myapp_user',
            db_password='',
            db_host='localhost',
            db_port='5432',
            verbose=False
        )

        self.database.create_connection()


    def run(self):
        self.running = True
    
        self.request()


    def stop(self):
        self.running = False


    def request(self):
        while self.running:
            if self.block == False:
                self.update_data()
            
            self.update_data_status()

            self.data_prev = self.data

            QThread.msleep(int(self.time_request))


    def update_data(self):
        self.data = self.database.read_data()
        self.update.emit(self.data)

        
    def update_data_change(self):
        self.data = self.database.read_data()

        if self.data_prev != None:
            for index, d in enumerate(self.data):
                if d != self.data_prev[index]:
                    print(f'Изменилось c {self.data_prev[index]} на {d}')
                    self.update.emit(self.data)
                    break

    
    def update_data_status(self):
        status_button = self.database.read_single_value('status')

        if status_button == 1 and app.threads.robot_filler.filler == False:
            self.button_start.emit()
            print('ВКОЮЧИТЬ')

        if status_button == 0 and app.threads.robot_filler.filler == True:
            self.button_stop.emit()
            print('ВЫКЛЮЧИТЬ')
                

    def block_on(self):
        self.block = True
        print('Block data')
    

    def block_off(self):
        self.block = False
        #self.update_data()
        print('UNBlock data')
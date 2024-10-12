import sys
from typing import List
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize, QTimer, QEvent
from PyQt5.QtGui import QCursor, QFontDatabase

#from Server.database import DatabaseManager
from Server2.server_control import ServerManager
from Server2.database_manager import DatabaseManager

from Filler_interface.Style_windows.style import Style



def enable_marker_decorator(marker_attr):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if getattr(self, marker_attr):
                return func(self, *args, **kwargs)
            else:
                print(f"{func.__name__} не выполнена, так как {marker_attr} == False")
        return wrapper
    return decorator



class App(QApplication):
    button_start = pyqtSignal()
    button_stop = pyqtSignal()

    button_calibration = pyqtSignal()
    button_panel = pyqtSignal()
    button_motor = pyqtSignal()


    def __init__(self) -> None:
        super().__init__(sys.argv)

        self.server = ServerManager()
        self.server.start_server()

        self.styling = Style()

        self.window_size = QSize(720, 480)

        self.on_fullscreen = False
        self.cursor_move_2 = True

        raspberry = True

        if raspberry:
            font_id = QFontDatabase.addApplicationFont("/usr/share/fonts/truetype/siemens_ad_vn.ttf")
            self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            self.font_family = 'Siemens AD Sans'

        self.lang_num = 0
        self.color = 'green'

        self.lang = 0

        self.window_focus = ''

        self.timer_datetime = QTimer()
        self.timer_datetime.timeout.connect(self.datetime)
        self.time_datetime = 210000
        self.timer_datetime.start(self.time_datetime)

        self.installEventFilter(self)

        self.ready = False

        # self.database = DatabaseManager('Server/myproject/db.sqlite3')

        self.database = DatabaseManager(
            db_name='myapp',
            db_user='myapp_user',
            db_password='',
            db_host='localhost',
            db_port='5432',
            verbose=False
        )

        self.database.create_connection()
        self.database_default()

        self.timer_database = QTimer()
        self.block_database = False
        self.timer_database.timeout.connect(self.database_update)
        self.time_database = 1000
        self.timer_database.start(self.time_database)

    
    def run(self):
        self.set_style()
        self.language()
        self.fullscreen()

        self.window_low.show()
        app.window_main_filler.show_animation()
        self.window_start.show_animation()

        sys.exit(app.exec_()) 
    

    def fullscreen(self):
        if self.on_fullscreen:
            self.window_start.fullscreen()
            self.window_datetime.fullscreen()
            self.window_low.fullscreen()
            self.window_main_filler.fullscreen()
            self.window_list1.fullscreen()
            self.window_settings2.fullscreen()
            self.window_prepare.fullscreen()
            self.window_view.fullscreen()
            self.window_filler.fullscreen()
            self.window_error.fullscreen()
            self.window_cip.fullscreen()
            self.window_robot.fullscreen()
            self.window_pop_up.fullscreen()


    def eventFilter(self, obj, event):
        # if self.cursor_move_2: 
        #     if event.type() == QEvent.MouseButtonRelease:
        #         QCursor.setPos(5, 5)

        #         # focus_widget = self.focusWidget()
                
        #         # if focus_widget:
        #         #     focus_widget.clearFocus()

        
        if event.type() == QEvent.MouseButtonPress:
            self.datetime_reset()
            self.database_reset()

            self.window_datetime.hide()

        return super().eventFilter(obj, event)
    

    def database_update(self):
        self.data_filler = self.database.read_data('myapp_filler')

        if self.block_database == False:
            
            self.window_robot.database_update()
            self.data_control = self.database.read_data('myapp_control')
            # print(self.data_control)
            
            if self.data_control[0][1] == True:
                self.button_calibration.emit()
                self.database.update_data('myapp_control', 'calibration', False)

            if self.data_control[0][2] == True: 
                self.threads.input_request.monitor_run = True
                self.database.update_data('myapp_control', 'panel', False)

            if self.data_control[0][3] == True:
                self.button_motor.emit()
                self.database.update_data('myapp_control', 'motor', False)


            # print('self.data_filler', self.data_filler)
            # print('self.data_robot', self.data_robot)

            self.window_filler.update_thread(self.data_filler[0])

        if self.data_filler[0][3] == True and self.window_filler.play == False: 
            self.button_start.emit()
            self.window_filler.play = True

        if self.data_filler[0][3] == False and self.window_filler.play == True: 
            self.button_stop.emit()
            self.window_filler.play = False
    

    def database_default(self):
        self.database.update_data('myapp_filler', 'status', False)
        self.database.update_data('myapp_control', 'calibration', False)
        self.database.update_data('myapp_control', 'panel', False)
        self.database.update_data('myapp_control', 'motor', False)

    
    def block_on(self):
        self.block_database = True
        #print('Block data')
    

    def block_off(self):
        self.block_database = False
        #print('UNBlock data')
    
    
    def database_reset(self):
        self.timer_database.stop()
        self.timer_database.start(self.time_database)


    def datetime(self):
        #app.window_datetime.show_window()
        app.window_start.show_2()
        

    def datetime_reset(self):
        self.timer_datetime.stop()
        self.timer_datetime.start(self.time_datetime)


    def language(self):
        lang_num = self.lang_num

        self.window_main_filler.language(lang_num)
        self.window_list1.language(lang_num)
        self.window_settings2.language(lang_num)
        self.window_prepare.language(lang_num)
        self.window_filler.language(lang_num)
        self.window_cip.language(lang_num)
        self.window_robot.language(lang_num)
        self.window_pop_up.language(lang_num)
        self.window_error.language(lang_num)


    def set_style(self):
        self.recolor()
        self.icons_recolor()


    def icons_recolor(self):
        self.styling.recolor_icons()
        
        self.window_main_filler.set_icons()
        self.window_list1.set_icons()
        # self.window_settings1.set_icons()
        self.window_settings2.set_icons()
        self.window_cip.set_icons()
        self.window_robot.set_icons()


    def recolor(self):
        style = self.styling.style()
        #style.recolor(self, (42, 122, 96, 255))
        style = self.styling.recolor_css(style)
        self.setStyleSheet(style)
    

    def create_windows(self):
        from Filler_interface.Window_start.start_conrtol import Start_control
        self.window_start = Start_control()

        from Filler_interface.Window_datetime.datetime_control import Datetime_control
        self.window_datetime = Datetime_control()

        # from Filler_interface.Window_pop_up.pop_up_control import window_pop_up
        # app.window_pop_up = window_pop_up

        from Filler_interface.Window_pop_up.pop_up_control2 import Confirm_control
        self.window_pop_up = Confirm_control()

        from Filler_interface.Window_low.low_control import Low_control
        self.window_low = Low_control()

        from Filler_interface.Window_main.main_filler_conrtol import Main_filler_control
        self.window_main_filler = Main_filler_control()

        from Filler_interface.Window_list1.list1_control import List_control
        self.window_list1 = List_control()

        from Filler_interface.Window_settings2.settings2_control import Settings_control
        self.window_settings2 = Settings_control()

        from Filler_interface.Window_prepare.prepare_control import Prepare_control
        self.window_prepare = Prepare_control()

        from Filler_interface.Window_view.view_conrtol import View_control
        self.window_view = View_control()

        from Filler_interface.Window_error.error_conrtol import Error_control
        self.window_error = Error_control()

        from Filler_interface.Window_cip.cip_control3 import Cip_control
        self.window_cip = Cip_control()

        from Filler_interface.Window_robot.robot_control3 import Robot_control
        self.window_robot = Robot_control()

        from Filler_interface.Window_filler.filler_control2 import Filler_control
        self.window_filler = Filler_control()

        self.ready = True

    
    def connected(self):
        from Threads.threads import Thread
        self.threads = Thread()

    
    def close_windows(self):
        if self.window_focus != self.window_start.window_name:
            self.window_start.hide()
            #print(f'close: {self.window_start.window_name}')
        
        if self.window_focus != self.window_datetime.window_name:
            self.window_datetime.hide()
            #print(f'close: {self.window_datetime.window_name}')
        
        # if self.window_focus != self.window_main_filler.window_name:
        #     self.window_main_filler.hide()
        #     print(f'close: {self.window_main_filler.window_name}')

        if self.window_focus != self.window_list1.window_name:
            self.window_list1.hide()
            #print(f'close: {self.window_list1.window_name}')

        if self.window_focus != self.window_settings2.window_name:
            self.window_settings2.hide()
            #print(f'close: {self.window_settings2.window_name}')

        if self.window_focus != self.window_prepare.window_name:
            self.window_prepare.hide()
            #print(f'close: {self.window_prepare.window_name}')

        if self.window_focus != self.window_view.window_name:
            self.window_view.close()
            #print(f'close: {self.window_view.window_name}')

        if self.window_focus != self.window_filler.window_name:
            self.window_filler.hide()
            #print(f'close: {self.window_filler.window_name}')

        if self.window_focus != self.window_error.window_name:
            self.window_error.hide()
            #print(f'close: {self.window_error.window_name}')

        if self.window_focus != self.window_cip.window_name:
            self.window_cip.hide()
            #print(f'close: {self.window_cip.window_name}')

        if self.window_focus != self.window_robot.window_name:
            self.window_robot.hide()
            #print(f'close: {self.window_robot.window_name}')


    def show_windows(self):
        match self.window_focus:
            case self.window_start.window_name:
                self.window_start.hide()
                self.window_start.show()

            case self.window_main_filler.window_name:
                self.window_main_filler.hide()
                self.window_main_filler.show()
            
            case self.window_list1.window_name:
                self.window_list1.show()

            case self.window_settings2.window_name:
                self.window_settings2.hide()
                self.window_settings2.show()

            case self.window_prepare.window_name:
                self.window_prepare.hide()
                self.window_prepare.show()
            
            case self.window_view.window_name:
                self.window_view.close(1)
                self.window_view.show()

            case self.window_filler.window_name:
                self.window_filler.hide()
                self.window_filler.show()

            case self.window_error.window_name:
                self.window_error.hide()
                self.window_error.show()

            case self.window_cip.window_name:
                self.window_cip.hide()
                self.window_cip.show()

            case self.window_robot.window_name:
                self.window_robot.hide()
                self.window_robot.show()


    def exit(self):
        sys.exit(self.exec_())
    

app = App()
app.create_windows()
app.connected()




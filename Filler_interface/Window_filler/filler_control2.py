from PyQt5.QtCore import QTimer, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import os

from Lib.memory import Memory
from Filler_interface.app import app

from Filler_interface.Window_filler.filler_template import Control


class Filler_control(Control):
    start_filler = pyqtSignal()
    stop_filler = pyqtSignal()


    def __init__(self):
        super().__init__()

        # self.database = DatabaseManager('Server/myproject/db.sqlite3')
        # self.database.create_connection()
        
        self.window_name = 'filler_control'

        icon_size = QSize(65, 65)
        button_size = QSize(140, 130)

        self.font_text = QFont()
        self.font_text.setFamily(app.font_family)
        self.font_text.setBold(False)
        self.font_text.setWeight(50)

        self.button_menu.setMinimumSize(button_size)
        #self.button_menu.setIconSize(icon_size)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(1000) 
        self.timer.timeout.connect(self.on_timer_timeout)

        self.step_button = 1

        self.button_menu.clicked.connect(self.button_menu_clicked)
        self.button_menu.pressed.connect(self.button_menu_pressed)
        self.button_menu.released.connect(self.button_menu_released)

        self.button_view.setMinimumSize(button_size)
        self.button_view.setIconSize(QSize(70, 70))

        self.button_view.clicked.connect(self.view)

        self.button_view.pressed.connect(self.button_view_pressed)
        self.button_view.released.connect(self.button_view_released)


        self.button_start.setMinimumSize(button_size)
        

        self.timer_left_pressed = QTimer(self)
        self.timer_left_pressed.setInterval(int(300/self.step_button))
        self.timer_left_pressed.timeout.connect(self.left)

        self.button_left.setMinimumSize(button_size)
        self.button_left.setIconSize(icon_size)

        self.button_left.clicked.connect(self.left)
        self.button_left.pressed.connect(self.left_pressed)
        self.button_left.released.connect(self.left_released)

        self.timer_right_pressed = QTimer(self)
        self.timer_right_pressed.setInterval(int(300/self.step_button))
        self.timer_right_pressed.timeout.connect(self.right)
        
        self.button_right.setMinimumSize(button_size)
        self.button_right.setIconSize(icon_size)

        self.button_right.clicked.connect(self.right)
        self.button_right.pressed.connect(self.right_pressed)
        self.button_right.released.connect(self.right_released)

        
        self.timer_minus_pressed = QTimer(self)
        self.timer_minus_pressed.setInterval(int(300/self.step_button))
        self.timer_minus_pressed.timeout.connect(self.minus)

        self.button_minus.setMinimumSize(button_size)
        self.button_minus.setIconSize(icon_size)

        self.button_minus.clicked.connect(self.minus)
        self.button_minus.pressed.connect(self.minus_pressed)
        self.button_minus.released.connect(self.minus_released)

        self.timer_plus_pressed = QTimer(self)
        self.timer_plus_pressed.setInterval(int(300/self.step_button))
        self.timer_plus_pressed.timeout.connect(self.plus)

        self.button_plus.setMinimumSize(button_size)
        self.button_plus.setIconSize(icon_size)

        self.button_plus.clicked.connect(self.plus)
        self.button_plus.pressed.connect(self.plus_pressed)
        self.button_plus.released.connect(self.plus_released)

        self.button_start.clicked.connect(self.button_start_clicked)

        self.button_start_marker = False

        self.set_icons()

        self.lang = 0
        self.step = 1

        self.param_num = 1
        self.value_id = 1

        self.param_list = []
        
        self.timer_exit = QTimer(self)
        self.timer_exit.setSingleShot(True)
        self.timer_exit.setInterval(6000) 
        self.timer_exit.timeout.connect(self.on_timer_reset)

        self.timer_button = QTimer(self)
        self.timer_button.setSingleShot(False)
        self.timer_button.setInterval(1000)
        self.timer_button.timeout.connect(self.button_recolor)

        file_path = os.path.join('Filler_interface', 'Window_settings1', 'Data')
        self.memory = Memory(db_path = file_path, db_file = 'memory_db')

        self.pump_value_1 = 50
        self.pump_value_2 = 50 
        self.min_value = 5

        self.prev_value1 = 0
        self.prev_value2 = 0
        
        self.param_list = self.get_parametrs()
        self.param_list = self.memory_read(self.param_list)
        self.put_parametrs()
        
        self.play = False

        self.file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-pause-button-100.png')
        self.file_path_new = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_start', 'icons8-pause-button-100.png')
        app.styling.recolor_image(self.file_path, self.file_path_new, (230, 160, 35))
        
        self.file_path_2 = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-circled-play-100.png')
        self.file_path_new_2 = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_start', 'icons8-circled-play-100.png')
        app.styling.recolor_image(self.file_path_2, self.file_path_new_2, (180, 70, 42))

        self.timer_button.start()

        self.update()
        self.button_start_update(0)
        self.enable_control()

        
    def show(self):
        super().show()
        self.play = False

        self.button_left.setEnabled(True)
        self.button_right.setEnabled(True)
        self.button_minus.setEnabled(True)
        self.button_plus.setEnabled(True)

        self.timer_button.start()

        self.update()


    def update(self):
        self.label_window_update()
        self.value_update()
        self.value_mini_update()
        #self.name_params_update()

        # self.button_start_update()
    
    
    def enable_control(self):
        self.minus_enable()
        self.plus_enable()
        self.left_enable()
        self.right_enable()
    

    def button_menu_clicked(self):
        super().button_menu_clicked()
        self.memory_write(self.param_list)
        
        # app.threads.robot_filler.robot.stop_motors()
        # app.threads.robot_filler.all_stop()

        self.play = False
        self.timer_button.stop()



    def button_view_pressed(self):
        pass


    def button_view_released(self):
        pass


    def on_timer_reset(self):
        pass


    def get_parametrs(self): 
        self.param_list = {
            1: self.pump_value_1,
            2: self.pump_value_2,
        }
    
        return self.param_list
    

    def memory_read(self, default):
        read = self.memory.memory_read('data', default)

        return read


    def put_parametrs(self):
        self.pump_value_1 = self.param_list[1]
        self.pump_value_2 = self.param_list[2]

        app.database.update_data('myapp_filler', 'drink1', self.param_list[1])
        app.database.update_data('myapp_filler', 'drink2', self.param_list[2])


    def memory_write(self, data):
        self.memory.memory_write('data', data)

    
    def view(self):
        app.window_list1.show()
        

    def label_window_update(self):
        pass
        # text = {
        #     0: 'НАПИТОК 1', 
        #     1: 'SYSTEM SETTINGS',
        #     2: 'SYSTEMEINSTELLUNGEN',
        #     3: '系統設定',
        # }
       

        # size_text = 30
        
        # text = text[self.lang]
        # self.label_window.setText(str(text))
        

        # font = QFont()
        # font.setFamily(app.font_family)
        # font.setPointSize(size_text)
        # font.setBold(False)
        # font.setWeight(50)
        # self.label_window.setFont(font)

        # text = {
        #     0: 'НАПИТОК 2', 
        #     1: 'SYSTEM SETTINGS',
        #     2: 'SYSTEMEINSTELLUNGEN',
        #     3: '系統設定',
        # }
       

        # size_text = 30
        
        # text = text[self.lang]
        # self.label_window_2.setText(str(text))
        

        # font = QFont()
        # font.setFamily(app.font_family)
        # font.setPointSize(size_text)
        # font.setBold(False)
        # font.setWeight(50)
        # self.label_window_2.setFont(font)


    def value_update(self):
        value_1 = self.param_list[1]
        value_2 = self.param_list[2]
        size_text = 70
    
        self.value.setText(str(f'1: {value_1}'))
        self.value_2.setText(str(f'2: {value_2}'))

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.value.setFont(font)
        self.value_2.setFont(font)

    
    def update_thread(self, data):
        self.param_list[1] = data[1]
        self.param_list[2] = data[2]

        self.put_parametrs()

        #print(f"UPDATE {self.param_list[1]} {self.param_list[2]}")

        self.value_update()


    def start_pump(self):
        self.value_pump_1 = self.param_list[1]
        self.value_pump_2 = self.param_list[2]

        self.prev_value1 = self.value_pump_1
        self.prev_value2 = self.value_pump_2

        self.button_left.setEnabled(False)
        self.button_right.setEnabled(False)
        self.button_minus.setEnabled(False)
        self.button_plus.setEnabled(False)


    def stop_pump(self): 
        self.prev_value1 = self.value_pump_2
        self.prev_value2 = self.value_pump_2
    
        self.value_update()

        self.button_left.setEnabled(True)
        self.button_right.setEnabled(True)
        self.button_minus.setEnabled(True)
        self.button_plus.setEnabled(True)

        self.min_value = 5


    def stop_pump_1(self):
        self.min_value = 0
        self.value_update_pump_1()

        self.min_value = 5
        


    def stop_pump_2(self):
        self.min_value = 0
        self.value_update_pump_2()

        self.min_value = 5


    def value_update_pump_1(self):
        step = 1000 * 0.0035
        #step = int(round(step, 0))
        self.value_pump_1 = self.value_pump_1 - step

        value_1 = int(round(self.value_pump_1 , 0))

        if value_1 <= self.min_value: 
            value_1 = self.min_value

        self.value.setText(str(f'1: {value_1}'))


    def value_update_pump_2(self):
        step = 1000 * 0.0035
        #step = int(round(step, 0))
        self.value_pump_2 = self.value_pump_2 - step

        value_2 = int(round(self.value_pump_2 , 0))

        if value_2 <= self.min_value: 
            value_2 = self.min_value 

        self.value_2.setText(str(f'2: {value_2}'))


    def value_update_pumps(self, value1, value2):
        if value1 <= 0: 
            value1 = 0

        if value2 <= 0: 
            value2 = 0

        if value1 <= self.prev_value1:
            self.prev_value1 = value1

        if value2 <= self.prev_value2:
            self.prev_value2 = value2
        
        value1 = int(value1)
        value2 = int(value2)

        #print('update', self.prev_value1, self.prev_value2)

        self.value.setText(str(f'1: {value1}'))
        self.value_2.setText(str(f'2: {value2}'))

    
    def value_mini_update(self):
        match self.param_num:
            case 1:
                text = {
                    0: 'мл',
                    1: 'ml',
                    2: 'ml',
                }

                size_text = 30
            case 2:
                text = {
                    0: 'мл',
                    1: 'ml',
                    2: 'ml',
                }

                size_text = 30
            case 3:
                text = {
                    0: 'мл',
                    1: 'ml',
                    2: 'ml',
                }

                size_text = 30
            case 4:
                text = {
                    0: 'мл',
                    1: 'ml',
                    2: 'ml',
                }

                size_text = 30
            case 5:
                text = {
                    0: '',
                    1: '',
                    2: '',
 
                }

                size_text = 30
            case _:
                text = {
                    0: '',
                    1: '',
                    2: '',
                }

                size_text = 30
        
        text = text[self.lang]
        self.value_mini.setText(str(text))
        self.value_mini_2.setText(str(text))

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.value_mini.setFont(font)
        self.value_mini_2.setFont(font)


    def name_params_update(self):
        match self.param_num:
            case 1:
                text = {
                    0: '40',
                    1: 'Volume 1 /ml',
                    2: '',
                    3: '',
                }

                size_text = 85
            case 2:
                text = {
                    0: 'Объем 2 бутылки',
                    1: 'Volume 2 /ml',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 3:
                text = {
                    0: 'Дозировка напитка 1',
                    1: 'Цвет 21 (Иконка)',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 4:
                text = {
                    0: 'Дозировка напитка 2',
                    1: 'Цвет 21 (Иконка)',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 5:
                text = {
                    0: 'Нажмите далее',
                    1: 'Нажмите далее 2',
                    2: '',
                    3: '',
                }

                size_text = 30
            case _:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
        
        text = text[self.lang]
        self.name_params.setText(str(text))

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.name_params.setFont(font)


    def minus(self):
        super().minus()

        self.enable_control()

        if self.param_list[1] >= 10:
            self.param_list[1] -= 10

        
        self.update()
        self.enable_control()

        self.put_parametrs()
       
        
    def minus_released(self):
        super().minus_released()

        match self.param_num:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
 
            
        self.update()

        self.put_parametrs()

        self.memory_write(self.param_list)


    def minus_enable(self):
        if self.param_list[1] <= 0:
            self.button_minus.setEnabled(False)
        else:
            self.button_minus.setEnabled(True)


    def plus(self):
        super().plus()

        self.enable_control()

        if self.param_list[1] < 500:
            self.param_list[1] += 10

        self.update()
        self.enable_control()

        self.put_parametrs()
    

    def plus_released(self):
        super().plus_released()

        match self.param_num:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass

        self.update()

        self.put_parametrs()

        self.memory_write(self.param_list)
        #print('pressed')


    def plus_enable(self):
        if self.param_list[1] >= 500:
            self.button_plus.setEnabled(False)
        else:
            self.button_plus.setEnabled(True)

    
    def left(self):
        super().left()

        self.enable_control()

        if self.param_list[2] >= 10:
            self.param_list[2] -= 10

        
        self.update()
        self.enable_control()

        self.put_parametrs()
     

    def left_enable(self):
        if self.param_list[2] <= 0:
            self.button_left.setEnabled(False)
        else:
            self.button_left.setEnabled(True)

    
    def left_released(self):
        super().left_released()

        self.put_parametrs()

        self.memory_write(self.param_list)


    def right(self):
        super().right()

        self.enable_control()

        if self.param_list[2] < 500:
            self.param_list[2] += 10

        self.update()
        self.enable_control()

        self.put_parametrs()


    def right_released(self):
        super().right_released()

        self.put_parametrs()

        self.memory_write(self.param_list)


    def right_enable(self):
        if self.param_list[1] >= 500:
            self.button_right.setEnabled(False)
        else:
            self.button_right.setEnabled(True)


    def button_start_update(self, state):
        # button_size = QSize(130, 120)
        # self.button_start.setFixedSize(button_size)
    
        icon_size = QSize(80, 80)
        self.button_start.setIconSize(icon_size)

        match state:
            case 0:
                if self.button_start_marker:
                    self.button_start.setIcon(QIcon(self.file_path_new_2))
                else:
                    self.button_start.setIcon(QIcon(self.file_path_2))

                # self.timer_button.start()
            case 1:
                self.button_start.setIcon(QIcon(self.file_path_new))
                # self.timer_button.stop()     

        
    def button_recolor(self):
        self.button_start_marker = not self.button_start_marker


    def button_start_clicked(self):
        self.play = not self.play
        # print('start')

        if self.play == True:
            self.start_filler.emit()
            app.database.update_data('myapp_filler', 'status', True)

            self.button_start_update(1)
        else:
            self.stop_filler.emit()
            app.database.update_data('myapp_filler', 'status', False)
            # app.threads.robot_filler.filler_stop()

            # app.threads.robot_filler.robot.stop_motors()
            # app.threads.robot_filler.all_stop()

            self.button_start_update(0)


               

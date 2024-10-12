from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtGui import QIcon, QFont
import os

from Lib.memory import Memory
from Filler_interface.app import app

from Filler_interface.Window_settings1.settings_template import Control

from Filler_interface.filler import filler


class Control(Control):
    def __init__(self):
        super().__init__()
        
        self.window_name = 'settings1'

        icon_size = QSize(70, 70)
        button_size = QSize(140, 130)

        self.font_text = QFont()
        self.font_text.setFamily(app.font_family)
        self.font_text.setBold(False)
        self.font_text.setWeight(50)

        self.button_menu.setMinimumSize(button_size)
        self.button_menu.setIconSize(icon_size)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(1000) 
        self.timer.timeout.connect(self.on_timer_timeout)

        self.button_menu.clicked.connect(self.button_menu_clicked)
        self.button_menu.pressed.connect(self.button_menu_pressed)
        self.button_menu.released.connect(self.button_menu_released)

        self.button_reset.setMinimumSize(button_size)
        self.button_reset.setIconSize(icon_size)

        self.button_reset.clicked.connect(self.show_popup)

        self.timer_left_pressed = QTimer(self)
        self.timer_left_pressed.setInterval(int(300))
        self.timer_left_pressed.timeout.connect(self.left)

        self.button_left.setMinimumSize(button_size)
        self.button_left.setIconSize(icon_size)

        self.button_left.clicked.connect(self.left)
        self.button_left.pressed.connect(self.left_pressed)
        self.button_left.released.connect(self.left_released)

        self.timer_right_pressed = QTimer(self)
        self.timer_right_pressed.setInterval(int(300))
        self.timer_right_pressed.timeout.connect(self.right)
        
        self.button_right.setMinimumSize(button_size)
        self.button_right.setIconSize(icon_size)

        self.button_right.clicked.connect(self.right)
        self.button_right.pressed.connect(self.right_pressed)
        self.button_right.released.connect(self.right_released)

        self.step_button = 1

        self.timer_minus_pressed = QTimer(self)
        self.timer_minus_pressed.setInterval(int(200/self.step_button))
        self.timer_minus_pressed.timeout.connect(self.minus)

        self.button_minus.setMinimumSize(button_size)
        self.button_minus.setIconSize(icon_size)

        self.button_minus.clicked.connect(self.minus)
        self.button_minus.pressed.connect(self.minus_pressed)
        self.button_minus.released.connect(self.minus_released)

        self.timer_plus_pressed = QTimer(self)
        self.timer_plus_pressed.setInterval(int(200/self.step_button))
        self.timer_plus_pressed.timeout.connect(self.plus)

        self.button_plus.setMinimumSize(button_size)
        self.button_plus.setIconSize(icon_size)

        self.button_plus.clicked.connect(self.plus)
        self.button_plus.pressed.connect(self.plus_pressed)
        self.button_plus.released.connect(self.plus_released)

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

        self.button_reset.pressed.connect(self.button_reset_pressed)
        self.button_reset.released.connect(self.button_reset_released)

        file_path = os.path.join('Filler_interface', 'Window_settings1', 'Data')
        self.memory = Memory(db_path = file_path, db_file = 'memory_db')
        
        self.param_list = self.get_parametrs()
        self.param_list = self.memory_read(self.param_list)
        self.put_parametrs()
        

        self.update()
        self.enable_control()


    def update(self):
        self.label_window_update()
        self.coll_params_update()
        self.value_update()
        self.value_mini_update()
        self.name_params_update()
    
    
    def enable_control(self):
        self.minus_enable()
        self.plus_enable()
        self.left_enable()
        self.right_enable()
    

    def button_menu_clicked(self):
        super().button_menu_clicked()
        self.memory_write(self.param_list)


    def button_reset_pressed(self):
        self.timer_exit.start()


    def button_reset_released(self):
        self.timer_exit.stop()


    def on_timer_reset(self):
        app.exit()


    def get_parametrs(self): 
        self.param_list = {
            1: filler.param3,
            2: filler.param4,
            3: filler.param5,
            4: filler.param6,
        }
    
        return self.param_list
    

    def memory_read(self, default):
        read = self.memory.memory_read('data', default)

        return read


    def put_parametrs(self):
        filler.param3 = self.param_list[1]
        filler.param4 = self.param_list[2]
        filler.param5 = self.param_list[3]
        filler.param6 = self.param_list[4]


    def memory_write(self, data):
        self.memory.memory_write('data', data)

    
    def default_parametrs(self):
        filler.param3 = 500
        filler.param4 = 600
        filler.param5 = 59
        filler.param6 = 60

        self.param_list = self.get_parametrs()
        self.memory_write(self.param_list)
        

    def label_window_update(self):
        match self.param_num:
            case 1:
                text = {
                    0: 'НАСТРОЙКА РОЗЛИВА', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case 2:
                text = {
                    0: 'НАСТРОЙКА РОЗЛИВА', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case 3:
                text = {
                    0: 'НАСТРОЙКА РОЗЛИВА', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case 4:
                text = {
                    0: 'НАСТРОЙКА РОЗЛИВА', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case 5:
                text = {
                    0: 'НАСТРОЙКА РОЗЛИВА', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
            case _:
                text = {
                    0: 'НАСТРОЙКА РОЗЛИВА', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                    3: '系統設定',
                }

                size_text = 21
        
        text = text[self.lang]
        self.label_window.setText(str(text))

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.label_window.setFont(font)


    def coll_params_update(self):
        size_text = 21
        
        text = f'{self.param_num} / {len(self.param_list) + 1}'
        self.coll_params.setText(str(text))

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.coll_params.setFont(font)


    def value_update(self):
        match self.param_num:
            case 1:
                value = self.param_list[self.param_num]
                size_text = 90
            case 2:
                value = self.param_list[self.param_num]
                size_text = 90
            case 3:
                value = self.param_list[self.param_num]
                size_text = 90
            case 4:
                value = self.param_list[self.param_num]
                size_text = 90
            case 5:
                value =  {
                    0: 'Готово',
                    1: 'Ready',
                    2: 'Sprache',
                    3: '語言',
                }

                value = value[self.lang]
                size_text = 70
            case _:
                value = None
                size_text = 60
        
        self.value.setText(str(value))

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.value.setFont(font)
    
    
    def value_mini_update(self):
        match self.param_num:
            case 1:
                text = {
                    0: 'мл',
                    1: 'ml',
                    2: 'ml',
                    3: '毫升',
                }

                size_text = 30
            case 2:
                text = {
                    0: 'мл',
                    1: 'ml',
                    2: 'ml',
                    3: '毫升',
                }

                size_text = 30
            case 3:
                text = {
                    0: 'мл',
                    1: 'ml',
                    2: 'ml',
                    3: '毫升',
                }

                size_text = 30
            case 4:
                text = {
                    0: 'мл',
                    1: 'ml',
                    2: 'ml',
                    3: '毫升',
                }

                size_text = 30
            case 5:
                text = {
                    0: '',
                    1: '',
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
        self.value_mini.setText(str(text))

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.value_mini.setFont(font)


    def name_params_update(self):
        match self.param_num:
            case 1:
                text = {
                    0: 'Объем 1 бутылки',
                    1: 'Volume 1 /ml',
                    2: '',
                    3: '',
                }

                size_text = 30
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

        match self.param_num:
            case 1:
                if self.param_list[self.param_num] >= 50:
                    self.param_list[self.param_num] -= 50
            case 2:
                if self.param_list[self.param_num] >= 50:
                    self.param_list[self.param_num] -= 50
            case 3:
                if self.param_list[self.param_num] >= 5:
                    self.param_list[self.param_num] -= 5
            case 4:
                if self.param_list[self.param_num] >= 5:
                    self.param_list[self.param_num] -= 5
            case 5:
                pass

        self.update()
        self.enable_control()
       
        
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

        self.memory_write(self.param_list)


    def minus_enable(self):
        match self.param_num:
            case 1:
                if self.param_list[self.param_num] <= 10:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 2:
                if self.param_list[self.param_num] <= 30:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 3:
                if self.param_list[self.param_num] <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 4:
                if self.param_list[self.param_num] <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 5:
                self.button_minus.setEnabled(False)


    def plus(self):
        super().plus()

        self.enable_control()

        match self.param_num:
            case 1:
                if self.param_list[self.param_num] < 1000:
                    self.param_list[self.param_num] += 50

                self.put_parametrs()
                
            case 2:
                if self.param_list[self.param_num] < 1200:
                    self.param_list[self.param_num] += 50
                
                self.put_parametrs()
                
            case 3:
                if self.param_list[self.param_num] < 100:
                    self.param_list[self.param_num] += 5
                
                self.put_parametrs()
                
            case 4:
                if self.param_list[self.param_num] < 120:
                    self.param_list[self.param_num] += 5
                
                self.put_parametrs()
                
            case 5:
                pass
                

        self.update()
        self.enable_control()
    

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

        self.memory_write(self.param_list)
        # print('pressed')


    def plus_enable(self):
        match self.param_num:
            case 1:
                if self.param_list[self.param_num] >= 1000:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 2:
                if self.param_list[self.param_num] >= 1200:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 3:
                if self.param_list[self.param_num] >= 100:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 4:
                if self.param_list[self.param_num] >= 120:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 5:
                self.button_plus.setEnabled(False)


    
    def left(self):
        if self.param_num > 1:
            self.param_num -= 1

        # print(self.param_num)

        self.enable_control()
        self.update()

        self.memory_write(self.param_list)
     

    def left_enable(self):
        if self.param_num <= 1:
            self.button_left.setEnabled(False)
        else:
            self.button_left.setEnabled(True)
    

    def right(self):
        if self.param_num < len(self.param_list) + 2:
            self.param_num += 1
        
        match self.param_num:
            case 6:
                app.window_prepare.show()
                self.hide()    


        self.enable_control()
        self.update()

        self.memory_write(self.param_list)


    def right_enable(self):
        if self.param_num >= len(self.param_list) + 2:
            self.button_right.setEnabled(False)
        else:
            self.button_right.setEnabled(True)

            


window_setting1 = Control()
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont
import os

from Filler_interface.app import app
from Filler_interface.filler import filler



class Control(QMainWindow):
    def __init__(self):
        super().__init__()

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface/Window_settings1', 'UI_settings.ui')
        # file_path = os.path.join('Filler_interface', 'Window_settings1', 'UI_settings.ui')
        uic.loadUi(file_path, self)
       
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        icon_size = QSize(60, 60)
        button_size = QSize(130, 120)

        self.font_text = QFont()
        self.font_text.setFamily("Siemens AD Sans")
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

        self.get_parametrs()

        self.set_parametrs()
        self.update_text()
        self.enable_control()

    
    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()
        
        self.param_num = 1
        self.update_text()
        self.enable_control()
        super().show()


    def button_menu_clicked(self):
        app.window_main_filler.show()
        self.hide()
    

    def button_menu_pressed(self):    
        self.timer.start()


    def button_menu_released(self):
        self.timer.stop()


    def on_timer_timeout(self):
        app.window_main_filler.show()
        self.hide()


    def show_popup(self):
        app.window_pop_up.hide()
        app.window_pop_up.show(self.reset)


    def reset(self):
        self.default_parametrs()
        self.set_parametrs()

        self.get_parametrs()

        self.update_text()
        self.enable_control()


    def language(self, lang):
        self.lang = lang

        self.update_text()

    
    def set_icons(self):
        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-menu-100.png')
        self.button_menu.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-replay-100.png')
        self.button_reset.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-back-100.png')
        self.button_left.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-forward-100.png')
        self.button_right.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-subtract-100.png')
        self.button_minus.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-plus-math-100.png')
        self.button_plus.setIcon(QIcon(file_path))


    def put_parametrs(self):
       filler.param1 = self.param_list[1]
       filler.param2 = self.param_list[2]
       filler.param3 = self.param_list[3]
       filler.param4 = self.param_list[4]
       filler.param5 = self.param_list[5]
       filler.param6 = self.param_list[6]

    
    def get_parametrs(self): 
        self.param_list = {
            1: filler.param1,
            2: filler.param2,
            3: filler.param3,
            4: filler.param4,
            5: filler.param5,
            6: filler.param6,
            7: 'Готово',
        }


    def default_parametrs(self):
        filler.param1 = filler.param1_def
        filler.param2 = filler.param2_def
        filler.param3 = filler.param3_def
        filler.param4 = filler.param4_def
        filler.param5 = filler.param5_def
        filler.param6 = filler.param6_def

    
    def set_parametrs(self):
        self.window_name = {
            1: ['Имя окна', 'Name window'],
            2: ['Имя окна', 'Name window'],
            3: ['Имя окна', 'Name window'],
            4: ['Имя окна', 'Name window'],
            5: ['Имя окна', 'Name window'],
            6: ['Имя окна', 'Name window'],
            7: ['Имя окна', 'Name window'],
        }   

        self.param_name = {
            1: ['Тип напитка 1', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
            2: ['Тип напитка 2', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
            3: ['Объем 1 бутылки', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
            4: ['Объем 2 бутылки', 'Volume 2 /ml', 'Volumen 2 /ml', '體積 2 /毫升'],
            5: ['Дозировка напитка 1', 'Volume 2 /ml', 'Volumen 2 /ml', '體積 2 /毫升'],
            6: ['Дозировка напитка 2', 'Volume 2 /ml', 'Volumen 2 /ml', '體積 2 /毫升'],
            7: ['Нажмите далее', 'Volume 2 /ml', 'Volumen 2 /ml', '體積 2 /毫升'],
        }

        self.font_size = {
            1: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            2: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            3: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            4: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            5: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            6: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            7: {'window_name': 21, 'coll_params': 35, 'value': 70, 'value_mini': 30, 'name_params': 30,},
        }

        self.value_name_mini = {
            1: ['', '', '', '', ''],
            2: ['', '', '', '', ''],
            3: ['мл', 'ml', 'ml', '毫升'],
            4: ['мл', 'ml', 'ml', '毫升'],
            5: ['мл', 'ml', 'ml', '毫升'],
            6: ['мл', 'ml', 'ml', '毫升'],
            7: ['', '', '', '', ''],
        }

        self.value_min = {
            1: None,
            2: None,
            3: 10,
            4: 30,
            5: 0,
            6: 0,
            7: None,
        }

        self.value_max = {
            1: None,
            2: None,
            3: 1000,
            4: 1200,
            5: 100,
            6: 100,
            7: None,
        }

        self.value_id = {
            1: 1,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
        }

        self.value_step = {
            1: [False, True],
            2: [False, True],
            3: 50,
            4: 50,
            5: 5,
            6: 5,
            7: [None],
        }

        self.value_name = {
            1: [['Нет', 'Да'], ['No', 'Yes']],
            2: [['Нет', 'Да'], ['No', 'Yes']],
            3: None,
            4: None,
            5: None,
            6: None,
            7: [['Готово', 'Ready']],
        }

        self.color_text = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
        }


    def text_color(self):
        color = self.color_text[self.param_num]

        #print('text_color')

        if color is not None:
            value_id = self.value_id[self.param_num]
            color = color[value_id]

            #print(value_id, color)

            if color is not None:
                color = color
            else:
                color = app.styling.text_color
        else:
            color = app.styling.text_color


        style = f"color: rgb({color[0]}, {color[1]}, {color[2]});"
        
        self.value.setStyleSheet(style)


    def update_text(self):
        self.text_color()

        size = self.font_size[self.param_num]['window_name']
        self.font_text.setPointSize(size)
        self.label_window.setFont(self.font_text)
        self.label_window.setText(self.window_name[self.param_num][self.lang])

        text = f'{self.param_num} / {len(self.param_list)}'
        self.coll_params.setText(text)
        size = self.font_size[self.param_num]['coll_params']
        self.font_text.setPointSize(size)
        self.coll_params.setFont(self.font_text)

        value = self.param_list[self.param_num]

        if isinstance(value, bool) or isinstance(value, str):
            value_id = self.value_id[self.param_num]
            
            if self.value_name[self.param_num] != None:
                value = self.value_name[self.param_num][self.lang][value_id]
            else:
                value = self.param_list[self.param_num]

            self.value.setText(f"{value}")
        elif isinstance(value, int) or isinstance(value, float):
            self.value.setText(f"{self.param_list[self.param_num]}")

        size = self.font_size[self.param_num]['value']
        self.font_text.setPointSize(size)
        self.value.setFont(self.font_text)

        self.value_mini.setText(f"{self.value_name_mini[self.param_num][self.lang]}")  
        size = self.font_size[self.param_num]['value_mini']
        self.font_text.setPointSize(size) 
        self.value_mini.setFont(self.font_text)

        self.name_params.setWordWrap(True)
        self.name_params.setText(f"{self.param_name[self.param_num][self.lang]}")
        size = self.font_size[self.param_num]['value_mini']
        self.font_text.setPointSize(size) 
        self.name_params.setFont(self.font_text)



    def value_mini_update(self):
        self.value_mini.setText(f"{self.value_name_mini[self.param_num][self.lang]}")  
        size = self.font_size[self.param_num]['value_mini']
        self.font_text.setPointSize(size) 
        self.value_mini.setFont(self.font_text)



    def enable_control(self):
        self.minus_enable()
        self.plus_enable()
        self.left_enable()
        self.right_enable()
        

    def left(self):
        if self.param_num > 1:
            self.param_num -= 1

        #print(self.param_num)

        self.enable_control()
        self.update_text()


    def left_pressed(self):
        self.timer_left_pressed.start()


    def left_released(self):
        self.timer_left_pressed.stop()

    
    def left_enable(self):
        if self.param_num <= 1:
            self.button_left.setEnabled(False)
        else:
            self.button_left.setEnabled(True)
        
    
    def right(self):
        if self.param_num < len(self.param_list):
            self.param_num += 1

        #print(self.param_num)

        self.enable_control()
        self.update_text()

    
    def right_pressed(self):
        self.timer_right_pressed.start()


    def right_released(self):
        self.timer_right_pressed.stop()

    
    def right_enable(self):
        if self.param_num > len(self.param_list):
            self.button_right.setEnabled(False)
        else:
            self.button_right.setEnabled(True)


    def minus(self):
        self.enable_control()

        self.timer_minus_pressed.setInterval(int(200/self.step_button))
        self.step_button += 0.1

        value = self.param_list[self.param_num]

        if isinstance(value, bool) or isinstance(value, str):
            value_id = self.value_id[self.param_num]

            if value_id > 0:
                self.value_id[self.param_num] -= 1
                value_id -= 1

            value = self.value_step[self.param_num][value_id]
            self.param_list[self.param_num] = value

            self.value.setText(f"{self.value_name[self.param_num][self.lang][value_id]}")
    
        elif isinstance(value, int) or isinstance(value, float):
            limit = self.value_min[self.param_num]
            
            self.step = self.value_step[self.param_num]

            if value >= limit:
                value -= self.step

            self.param_list[self.param_num] = value
        
            self.value.setText(f"{value}")

        self.update_text()
        self.enable_control()
        self.put_parametrs()


    def minus_pressed(self):
        self.timer_minus_pressed.start()


    def minus_released(self):
        self.timer_minus_pressed.stop()
        self.step_button = 1


    def minus_enable(self):
        value = self.param_list[self.param_num]

        # print(value, type(value))

        if isinstance(value, bool) or isinstance(value, str):
            value_id = self.value_id[self.param_num]

            if value_id <= 0:
                self.button_minus.setEnabled(False)
            else:
                self.button_minus.setEnabled(True)

        elif isinstance(value, int) or isinstance(value, float):
            self.step = self.value_step[self.param_num]

            # print(self.param_list[self.param_num], self.param_list)
            
            if value < self.step:
                self.button_minus.setEnabled(False)
            else:
                self.button_minus.setEnabled(True)


    def plus(self):
        self.timer_plus_pressed .setInterval(int(200/self.step_button))
        self.step_button += 0.1
    
        self.enable_control()

        value = self.param_list[self.param_num]

        if isinstance(value, bool) or isinstance(value, str):
            value_id = self.value_id[self.param_num]
            
            if value_id < len(self.value_step[self.param_num]) - 1:
                self.value_id[self.param_num] += 1 
                value_id += 1

            value = self.value_step[self.param_num][value_id]
            self.param_list[self.param_num] = value

            self.value.setText(f"{self.value_name[self.param_num][self.lang][value_id]}")
    
        elif isinstance(value, int) or isinstance(value, float):
            limit = self.value_max[self.param_num]

            self.step = self.value_step[self.param_num]

            if value < limit:
                value += self.step

            self.param_list[self.param_num] = value
        
            self.value.setText(f"{value}")

        self.update_text()
        self.enable_control()
        self.put_parametrs()


    def plus_pressed(self):
        self.timer_plus_pressed.start()


    def plus_released(self):
        self.timer_plus_pressed.stop()
        self.step_button = 1


    def plus_enable(self):
        value = self.param_list[self.param_num]


        if isinstance(value, bool) or isinstance(value, str):
            value_id = self.value_id[self.param_num]

            if value_id >= len(self.value_step[self.param_num]) - 1:
                self.button_plus.setEnabled(False)
            else:
                self.button_plus.setEnabled(True)

        elif isinstance(value, int) or isinstance(value, float):
            limit = self.value_max[self.param_num]
            self.step = self.value_step[self.param_num]

            if value >= limit:
                self.button_plus.setEnabled(False)
            else:
                self.button_plus.setEnabled(True)



window_setting = Control()
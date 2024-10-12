from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtGui import QIcon, QFont
import os

from Lib.memory import Memory
from Filler_interface.app import app

from Filler_interface.Window_settings1.settings_template import Control


class Settings_control(Control):
    def __init__(self):
        super().__init__()

        self.window_name = 'setting2'

        icon_size = QSize(65, 65)
        button_size = QSize(140, 130)

        self.font_text = QFont()
        self.font_text.setFamily(app.font_family)
        self.font_text.setBold(False)
        self.font_text.setWeight(50)

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
        self.timer_left_pressed.setInterval(int(500))
        self.timer_left_pressed.timeout.connect(self.left)

        self.button_left.setMinimumSize(button_size)
        self.button_left.setIconSize(icon_size)

        self.button_left.clicked.connect(self.left)
        self.button_left.pressed.connect(self.left_pressed)
        self.button_left.released.connect(self.left_released)

        self.timer_right_pressed = QTimer(self)
        self.timer_right_pressed.setInterval(int(500))
        self.timer_right_pressed.timeout.connect(self.right)
        
        self.button_right.setMinimumSize(button_size)
        self.button_right.setIconSize(icon_size)

        self.button_right.clicked.connect(self.right)
        self.button_right.pressed.connect(self.right_pressed)
        self.button_right.released.connect(self.right_released)

        self.step_button = 1

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

        
        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Window_settings2', 'Data')
        self.memory = Memory(db_path = file_path, db_file = 'memory_db')
        
        self.param_list = self.get_parametrs()
        self.param_list = self.memory_read(self.param_list)
        self.put_parametrs()
        

        self.update()
        self.enable_control()


    def show_popup(self):
        app.window_pop_up.hide()
        app.window_pop_up.show(self.reset)

        pop_show_text = {
            0: 'Вы хотите сделать параметры по умолчанию?',
            1: 'Do you want to make the settings default?',
            2: 'Möchten Sie die Einstellungen als Standard festlegen?',
        }

        app.window_pop_up.label_2.setText(pop_show_text[self.lang])


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
        app.server.stop_server()
        app.exit()


    def get_parametrs(self): 
        self.param_list = {
            1: app.lang_num,
            2: app.styling.r_border,
            3: app.styling.g_border,
            4: app.styling.b_border,
            5: app.styling.r_icons_text,
            6: app.styling.g_icons_text,
            7: app.styling.b_icons_text,
        }
    
        return self.param_list
    

    def memory_read(self, default):
        read = self.memory.memory_read('data', default)

        return read


    def put_parametrs(self):
        app.lang_num = self.param_list[1]
        app.styling.r_border = self.param_list[2]
        app.styling.g_border = self.param_list[3]
        app.styling.b_border = self.param_list[4]
        app.styling.r_icons_text = self.param_list[5]
        app.styling.g_icons_text = self.param_list[6]
        app.styling.b_icons_text = self.param_list[7]


    def memory_write(self, data):
        self.memory.memory_write('data', data)

    
    def default_parametrs(self):
        self.memory.recreate_database()

        app.lang_num = 2
        app.styling.r_border = 108
        app.styling.g_border = 170
        app.styling.b_border = 210
        app.styling.r_icons_text = 108
        app.styling.g_icons_text = 178
        app.styling.b_icons_text = 149

        self.param_list = self.get_parametrs()
        self.memory_write(self.param_list)
        
        app.language()
        app.icons_recolor()
        app.recolor()
    

    def label_window_update(self):
        match self.param_num:
            case 1:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                }

                size_text = 25
            case 2:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                }

                size_text = 25
            case 3:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                }

                size_text = 25
            case 4:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                }

                size_text = 25
            case 5:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                }

                size_text = 25
            case 6:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                }

                size_text = 25
            case 7:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN',
                }

                size_text = 25
            case _:
                text = {
                    0: 'НАСТРОЙКИ СИСТЕМЫ', 
                    1: 'SYSTEM SETTINGS',
                    2: 'SYSTEMEINSTELLUNGEN'
                }

                size_text = 25
        
        text = text[self.lang]
        self.label_window.setText(str(text))

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.label_window.setFont(font)


    def coll_params_update(self):
        size_text = 23
        
        text = f'{self.param_num} / {len(self.param_list)}'
        self.coll_params.setText(str(text))

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.coll_params.setFont(font)


    def value_update(self):
        value = self.param_list[self.param_num]

        match self.param_num:
            case 1:
        
                value_text = {0: 'Русский', 
                              1: 'English', 
                              2: 'Deutsch', 
                              }

                value = value_text[int(value)]

                size_text = 60
            case 2:

                value = f"R:{value}"

                size_text = 60
            case 3:

                value = f"G:{value}"

                size_text = 60
            case 4:
 
                value = f"B:{value}"

                size_text = 60
            case 5:

                value = f"R:{value}"

                size_text = 60
            case 6:

                value = f"G:{value}"

                size_text = 60
            case 7:

                value = f"B:{value}"

                size_text = 60
            case 8:

                value = f"R:{value}"

                size_text = 60
            case 9:

                value = f"G:{value}"

                size_text = 60
            case 10:

                value = f"B:{value}"

                size_text = 60
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
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 2:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 3:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 4:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
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
            case 6:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 30
            case 7:
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
                    0: 'Язык',
                    1: 'Language',
                    2: 'Sprache',
                }

                size_text = 35
            case 2:
                text = {
                    0: 'Цвет контура (R,G,B)',
                    1: 'Outline color (R,G,B)',
                    2: 'Umrissfarbe (R,G,B)'
                }

                size_text = 35
            case 3:
                text = {
                    0: 'Цвет контура (R,G,B)',
                    1: 'Outline color (R,G,B)',
                    2: 'Umrissfarbe (R,G,B)'
                }

                size_text = 35
            case 4:
                text = {
                    0: 'Цвет контура (R,G,B)',
                    1: 'Outline color (R,G,B)',
                    2: 'Umrissfarbe (R,G,B)'
                }

                size_text = 35
            case 5:
                text = {
                    0: 'Цвет иконок (R,G,B)',
                    1: 'Color of icons',
                    2: 'Farbe der Symbole',
                }

                size_text = 35
            case 6:
                text = {
                    0: 'Цвет иконок (R,G,B)',
                    1: 'Color of icons (R,G,B)',
                    2: 'Farbe der Symbole (R,G,B)',
                }

                size_text = 35
            case 7:
                text = {
                    0: 'Цвет иконок (R,G,B)',
                    1: 'Color of icons (R,G,B)',
                    2: 'Farbe der Symbole (R,G,B)',
                }

                size_text = 35

            case 8:
                text = {
                    0: 'Цвет 3 (Текст)',
                    1: 'Цвет 31 (Текст)',
                    2: '',
                    3: '',
                }

                size_text = 35
            case 9:
                text = {
                    0: 'Цвет 3 (Текст)',
                    1: 'Цвет 31 (Текст)',
                    2: '',
                    3: '',
                }

                size_text = 35
            case 10:
                text = {
                    0: 'Цвет 3 (Текст)',
                    1: 'Цвет 31 (Текст)',
                    2: '',
                    3: '',
                }

                size_text = 35
            case _:
                text = {
                    0: '',
                    1: '',
                    2: '',
                    3: '',
                }

                size_text = 35
        
        text = text[self.lang]
        self.name_params.setText(str(text))

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(size_text)
        font.setBold(False)
        font.setWeight(50)
        self.name_params.setFont(font)
        self.name_params.setWordWrap(True)


    def minus(self):
        super().minus()

        self.enable_control()

        match self.param_num:
            case 1:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1
                
                self.put_parametrs()
                app.language()
            case 2:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1
                
                self.put_parametrs()
                app.recolor()
            case 3:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1
                
                self.put_parametrs()
                app.recolor()
            case 4:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1
                
                self.put_parametrs()
                app.recolor()
            case 5:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1

                self.put_parametrs()
                app.recolor()
            case 6:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1

                self.put_parametrs()
                app.recolor()
            case 7:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1

                self.put_parametrs()
                app.recolor()
            case 8:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1

                self.put_parametrs()
                app.recolor()
            case 9:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1

                self.put_parametrs()
                app.recolor()
            case 10:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1

                self.put_parametrs()
                app.recolor()

        self.update()
        self.enable_control()
       
        
    def minus_released(self):
        super().minus_released()

        match self.param_num:
            case 1:
                pass

            case 2:
                app.icons_recolor()
                app.recolor()

            case 3:
                app.icons_recolor()
                app.recolor()

            case 4:
                app.icons_recolor()
                app.recolor()

            case 5:
                app.icons_recolor()
                app.recolor()

            case 6:
                app.icons_recolor()
                app.recolor()

            case 7:
                app.icons_recolor()
                app.recolor()

            case 8:
                app.icons_recolor()
                app.recolor()

            case 9:
                app.icons_recolor()
                app.recolor()

            case 10:
                app.icons_recolor()
                app.recolor()

        self.update()

        self.memory_write(self.param_list)


    def minus_enable(self):
        match self.param_num:
            case 1:
                if self.param_list[self.param_num] <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 2:
                if self.param_list[self.param_num] <= 0:
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
                if self.param_list[self.param_num] <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 6:
                if self.param_list[self.param_num] <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 7:
                if self.param_list[self.param_num] <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 8:
                if self.param_list[self.param_num] <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 9:
                if self.param_list[self.param_num] <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 10:
                if self.param_list[self.param_num] <= 0:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)


    def plus(self):
        super().plus()

        self.enable_control()

        match self.param_num:
            case 1:
                if self.param_list[self.param_num] < 3:
                    self.param_list[self.param_num] += 1
                
                self.put_parametrs()
                app.language()
            case 2:
                if self.param_list[self.param_num] < 255:
                    self.param_list[self.param_num] += 1
                    
                self.put_parametrs()
                app.recolor()
            case 3:
                if self.param_list[self.param_num] < 255:
                    self.param_list[self.param_num] += 1

                self.put_parametrs()
                app.recolor()
            case 4:
                if self.param_list[self.param_num] < 255:
                    self.param_list[self.param_num] += 1
                
                self.put_parametrs()
                app.recolor()
            case 5:
                if self.param_list[self.param_num] < 255:
                    self.param_list[self.param_num] += 1
                
                self.put_parametrs()
                app.recolor()
            case 6:
                if self.param_list[self.param_num] < 255:
                    self.param_list[self.param_num] += 1
                
                self.put_parametrs()
                app.recolor()
            case 7:
                if self.param_list[self.param_num] < 255:
                    self.param_list[self.param_num] += 1
                
                self.put_parametrs()
                app.recolor()
            case 8:
                if self.param_list[self.param_num] < 255:
                    self.param_list[self.param_num] += 1
                
                self.put_parametrs()
                app.recolor()
            case 9:
                if self.param_list[self.param_num] < 255:
                    self.param_list[self.param_num] += 1
                
                self.put_parametrs()
                app.recolor()
            case 10:
                if self.param_list[self.param_num] < 255:
                    self.param_list[self.param_num] += 1
                
                self.put_parametrs()
                app.recolor()

        self.update()
        self.enable_control()


    def plus_released(self):
        super().plus_released()

        match self.param_num:
            case 1:
                pass

            case 2:
                app.icons_recolor()
                app.recolor()

            case 3:
                app.icons_recolor()
                app.recolor()

            case 4:
                app.icons_recolor()
                app.recolor()

            case 5:
                app.icons_recolor()
                app.recolor()

            case 6:
                app.icons_recolor()
                app.recolor()

            case 7:
                app.icons_recolor()
                app.recolor()

            case 8:
                app.icons_recolor()
                app.recolor()

            case 9:
                app.icons_recolor()
                app.recolor()

            case 10:
                app.icons_recolor()
                app.recolor()

        self.update()

        self.memory_write(self.param_list)


    def plus_enable(self):
        match self.param_num:
            case 1:
                if self.param_list[self.param_num] >= 2:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 2:
                if self.param_list[self.param_num] >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 3:
                if self.param_list[self.param_num] >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 4:
                if self.param_list[self.param_num] >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 5:
                if self.param_list[self.param_num] >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 6:
                if self.param_list[self.param_num] >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 7:
                if self.param_list[self.param_num] >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 8:
                if self.param_list[self.param_num] >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 9:
                if self.param_list[self.param_num] >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 10:
                if self.param_list[self.param_num] >= 255:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

    
    def left(self):
        if self.param_num > 1:
            self.param_num -= 1

        self.enable_control()
        self.update()

        self.memory_write(self.param_list)
     

    def left_enable(self):
        if self.param_num <= 1:
            self.button_left.setEnabled(False)
        else:
            self.button_left.setEnabled(True)
    

    def right(self):
        if self.param_num < len(self.param_list):
            self.param_num += 1

        self.enable_control()
        self.update()

        self.memory_write(self.param_list)


    def right_enable(self):
        if self.param_num >= len(self.param_list):
            self.button_right.setEnabled(False)
        else:
            self.button_right.setEnabled(True)
            
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont
import os

from Filler_interface.app import app, enable_marker_decorator


class Control(QMainWindow):
    def __init__(self):
        super().__init__()
        
        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface/Window_settings1', 'UI_settings.ui')
        # file_path = os.path.join('Filler_interface', 'Window_settings1', 'UI_settings.ui')
        uic.loadUi(file_path, self)
       
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.pressed_minus = QTimer(self)
        self.pressed_minus.setInterval(1000)
        self.pressed_minus.timeout.connect(self.minus_pressed_2)

        self.pressed_plus = QTimer(self)
        self.pressed_plus.setInterval(1000)
        self.pressed_plus.timeout.connect(self.plus_pressed_2)

        button_size = QSize(140, 130)
        
        self.button_menu.setMinimumSize(button_size)
        self.button_menu.setIconSize(QSize(76, 76))

        self.timer_enable = QTimer(self)
        self.timer_enable.setSingleShot(True) 
        self.timer_enable.timeout.connect(self.all_enable_on)
        self.timer_enable.start(1000) 
        self.enable_marker = True

    
    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()
        self.param_num = 1
        
        self.update()
        self.enable_control()
        super().show()

        app.window_focus = self.window_name
        # print(app.window_focus)
        #app.close_windows()

        self.setFocus()

        self.all_enable_off()


    def all_enable_on(self):
        self.enable_marker = True

    
    def all_enable_off(self):
        self.enable_marker = False
        self.timer_enable.start()


    def button_menu_clicked(self):
        pass
    
    
    @enable_marker_decorator('enable_marker')
    def button_menu_pressed(self):    
        self.timer.start()


    @enable_marker_decorator('enable_marker')
    def button_menu_released(self):
        app.window_main_filler.show()
        self.hide()
    
        self.timer.stop()


    def on_timer_timeout(self):
        app.window_main_filler.show()
        self.hide()


    def show_popup(self):
        app.window_pop_up.hide()
        app.window_pop_up.show(self.reset)


    def reset(self):
        self.default_parametrs()

        self.update()
        self.enable_control()


    def language(self, lang):
        self.lang = int(lang)

        self.update()

    
    def set_icons(self):
        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-закрыть-окно-96')
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
        pass

    
    def get_parametrs(self): 
        pass


    def default_parametrs(self):
        pass
    

    def text_color(self, color):
        if color is None:
            color = app.styling.text_color

        style = f"color: rgb({color[0]}, {color[1]}, {color[2]});"
        
        self.value.setStyleSheet(style)


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


    def label_window_update(self):
        pass


    def coll_params_update(self):
        pass


    def value_update(self):
        pass


    def value_mini_update(self):
        pass


    def name_params_update(self):
        pass


    def left(self):
        pass

    def left_pressed(self):
        #self.timer_left_pressed.start()
        pass


    def left_released(self):
        #self.timer_left_pressed.stop()
        pass

    
    def left_enable(self):
        pass
    

    def right(self):
        pass
    

    def right_pressed(self):
        #self.timer_right_pressed.start()
        pass


    def right_released(self):
        #self.timer_right_pressed.stop()
        pass

    
    def right_enable(self):
        pass


    def minus(self):
        self.timer_minus_pressed.setInterval(int(1000/(1 + self.step_button)))
        self.step_button += 0.2


    def minus_pressed(self):
        self.pressed_minus.start()

    
    def minus_pressed_2(self):
        self.timer_minus_pressed.start()
        self.pressed_minus.stop()


    def minus_released(self):
        self.pressed_minus.stop()
        self.timer_minus_pressed.stop()
        self.step_button = 1


    def minus_enable(self):
        pass


    def plus(self):
        self.timer_plus_pressed.setInterval(int(1000/(1 + self.step_button)))
        self.step_button += 0.2


    def plus_pressed(self):
        self.pressed_plus.start()


    def plus_pressed_2(self):
        self.pressed_plus.stop()
        self.timer_plus_pressed.start()


    def plus_released(self):
        self.pressed_plus.stop()
        self.timer_plus_pressed.stop()
        self.step_button = 1


    def plus_enable(self):
        pass


window_setting = Control()
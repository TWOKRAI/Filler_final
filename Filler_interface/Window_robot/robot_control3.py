from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtGui import QIcon, QFont
import os

from Lib.memory import Memory
from Filler_interface.app import app, enable_marker_decorator

from Filler_interface.Window_settings1.settings_template import Control


class Robot_control(Control):
    def __init__(self):
        super().__init__()

        self.window_name = 'robot'

        icon_size = QSize(65, 65)
        button_size = QSize(140, 130)

        self.font_text = QFont()
        self.font_text.setFamily(app.font_family)
        self.font_text.setBold(False)
        self.font_text.setWeight(50)

        self.button_menu.setMinimumSize(button_size)
        # self.button_menu.setIconSize(icon_size)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(1000) 
        self.timer.timeout.connect(self.on_timer_timeout)

        self.button_menu.clicked.connect(self.button_menu_clicked)
        self.button_menu.pressed.connect(self.button_menu_pressed)
        self.button_menu.released.connect(self.button_menu_released)

        self.button_reset.setMinimumSize(button_size)
        self.button_reset.setIconSize(icon_size)

        self.button_reset.released.connect(self.show_popup)

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

        self.speed_robot = 70
        self.time_robot = 5
        self.laser_mode = 2
        self.autovalue = 1
        self.presence_cup = 1

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Window_robot', 'Data')
        self.memory = Memory(db_path = file_path, db_file = 'memory_db')

        self.param_list = self.get_parametrs()
        #self.param_list = self.memory_read(self.param_list)
        self.put_parametrs()

        self.update()
        self.enable_control()

    
    def show(self):
        self.get_parametrs()
        super().show()


    def show_popup(self):
        app.window_pop_up.hide()
        app.window_pop_up.show(self.reset)

        pop_show_text = {
            0: 'Вы хотите сделать параметры по умолчанию?',
            1: 'Do you want to make the settings default?',
            2: 'Möchten Sie die Einstellungen als Standard festlegen?',
        }

        app.window_pop_up.label_2.setText(pop_show_text[self.lang])

        self.setFocus()


    def update(self):
        self.label_window_update()
        self.coll_params_update()
        self.value_update()
        self.value_mini_update()
        self.name_params_update()
        self.enable_control()
    
    
    def enable_control(self):
        self.minus_enable()
        self.plus_enable()
        self.left_enable()
        self.right_enable()
    

    def button_menu_clicked(self):
        super().button_menu_clicked()

        self.put_parametrs()

        self.memory_write(self.param_list)
        

    @enable_marker_decorator('enable_marker')
    def button_reset_pressed(self):
        self.timer_exit.start()


    @enable_marker_decorator('enable_marker')
    def button_reset_released(self):
        self.timer_exit.stop()
        self.setFocus()


    def on_timer_reset(self):
        app.exit()

    
    def database_update(self):
        self.get_parametrs()
        self.update()


    def get_parametrs(self): 
        self.data_robot = app.database.read_data('myapp_robot')
        #print('self.data_robot', self.data_robot)

        self.speed_robot = self.data_robot[0][1]
        self.time_robot = self.data_robot[0][2]
        self.laser_mode = self.data_robot[0][3]
        self.autovalue = int(self.data_robot[0][4])
        self.presence_cup = int(self.data_robot[0][5])

        #print( 'GET robot myapp_robot', self.speed_robot, self.time_robot, self.laser_mode, self.autovalue, self.presence_cup)

        self.param_list = {
            1: self.speed_robot,
            2: self.time_robot,
            3: self.laser_mode,
            4: self.autovalue,
            5: self.presence_cup,
        }
    
        return self.param_list
    

    def memory_read(self, default):
        read = self.memory.memory_read('data', default)

        return read


    def put_parametrs(self):
        # speed = (100 - self.param_list[1]) / 50000
        # self.speed_robot = round(speed, 6)
        
        self.speed_robot = self.param_list[1]
        self.time_robot = self.param_list[2]
        self.laser_mode = self.param_list[3]
        self.autovalue = self.param_list[4]
        self.presence_cup = self.param_list[5]

        self.autovalue = bool(self.autovalue)
        self.presence_cup = bool(self.presence_cup)

        # print( 'PUT robot myapp_robot', self.param_list[1], self.time_robot, self.laser_mode, self.autovalue, self.presence_cup)

        app.database.update_data('myapp_robot', 'speed', self.param_list[1])
        app.database.update_data('myapp_robot', 'time_wait', self.time_robot)
        app.database.update_data('myapp_robot', 'laser_mode', self.laser_mode)
        app.database.update_data('myapp_robot', 'autovalue', self.autovalue)
        app.database.update_data('myapp_robot', 'presence_cup', self.presence_cup)


    def memory_write(self, data):
        # self.memory.memory_write('data', data)

        self.put_parametrs()

    
    def default_parametrs(self):
        self.memory.recreate_database()

        self.speed_robot = 70
        self.time_robot = 5
        self.laser_mode = 2
        self.autovalue = 1
        self.presence_cup = 1

        self.param_list = self.get_parametrs()
        self.memory_write(self.param_list)
        
        app.language()
        app.icons_recolor()
        app.recolor()
    

    def label_window_update(self):
        match self.param_num:
            case 1:
                text = {
                    0: 'НАСТРОЙКИ РОБОТА', 
                    1: 'ROBOT SETTINGS',
                    2: 'ROBOTEREINSTELLUNGEN',
                }

                size_text = 25
            case 2:
                text = {
                    0: 'НАСТРОЙКИ РОБОТА', 
                    1: 'ROBOT SETTINGS',
                    2: 'ROBOTEREINSTELLUNGEN',
                }

                size_text = 25
            case 3:
                text = {
                    0: 'НАСТРОЙКИ РОБОТА', 
                    1: 'ROBOT SETTINGS',
                    2: 'ROBOTEREINSTELLUNGEN',
                }

                size_text = 25
            
            case 4:
                text = {
                    0: 'НАСТРОЙКИ РОБОТА', 
                    1: 'ROBOT SETTINGS',
                    2: 'ROBOTEREINSTELLUNGEN',
                }

                size_text = 25

            case 5:
                text = {
                    0: 'НАСТРОЙКИ РОБОТА', 
                    1: 'ROBOT SETTINGS',
                    2: 'ROBOTEREINSTELLUNGEN',
                }

                size_text = 25

            case _:
                text = {
                    0: 'НАСТРОЙКИ РОБОТА', 
                    1: 'ROBOT SETTINGS',
                    2: 'ROBOTEREINSTELLUNGEN',
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
        size_text = 25
        
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
                value = value

                size_text = 90
            case 2:

                value = value

                size_text = 90
            case 3:
                value = value

                size_text = 90
            
            case 4:
                value_text = [
                    ['Выкл', 'Off', 'Aus'],
                    ['Вкл', 'On', 'An'],
                    ]

                value = value_text[value]
                value = value[self.lang]
        
                size_text = 90
            
            case 5:
                value_text = [
                    ['Выкл', 'Off', 'Aus'],
                    ['Вкл', 'On', 'An'],
                    ]

                value = value_text[value]
                value = value[self.lang]
        
                size_text = 90
               
            case _:
                value = None

                size_text = 90
        
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
                }

                size_text = 35
            case 2:
                text = {
                    0: 'сек.',
                    1: 'sec.',
                    2: 'sek.',
                }

                size_text = 35
            case 3:
                text = {
                    0: '',
                    1: '',
                    2: '',
                }

                size_text = 35
            
            case 4:
                text = {
                    0: '',
                    1: '',
                    2: '',
                }

                size_text = 35

            case 5:
                text = {
                    0: '',
                    1: '',
                    2: '',
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
                    0: 'Робот: скорость',
                    1: 'Robot: speed',
                    2: 'Roboter: Geschwindigkeit',
                }

                size_text = 35
            case 2:
                text = {
                    0: 'Время ожидания после налива',
                    1: 'Waiting time after pouring',
                    2: 'Wartezeit nach dem Befüllen',
                }

                size_text = 35
            case 3:
                text = {
                    0: 'Режим лазера',
                    1: 'Laser mode',
                    2: 'Lasermodus',
                    3: '',
                }

                size_text = 35

            case 4:
                text = {
                    0: 'Автообъем для ограничения',
                    1: 'Auto volume for limitation',
                    2: 'Automatisches Volumen zur Begrenzung',
                }

                size_text = 29
            
            case 5:
                text = {
                    0: 'Проверка наличия стакана',
                    1: 'Check for the presence of a glass',
                    2: 'Überprüfung auf das Vorhandensein eines Glases',
                }

                size_text = 29
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
                if self.param_list[self.param_num] > 1:
                    self.param_list[self.param_num] -= 1
                
                self.put_parametrs()
                app.language()
            case 2:
                if self.param_list[self.param_num] > 1:
                    self.param_list[self.param_num] -= 1
                
                self.put_parametrs()
                app.recolor()
            case 3:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1

                self.put_parametrs()
            case 4:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1

                self.put_parametrs()
            case 5:
                if self.param_list[self.param_num] > 0:
                    self.param_list[self.param_num] -= 1
                  
                self.put_parametrs()


        self.update()
        self.enable_control()

        # print('click') 
       
    
    @enable_marker_decorator('enable_marker')
    def minus_released(self):
        super().minus_released()
        self.setFocus()

        match self.param_num:
            case 1:
                pass

            case 2:
                pass

            case 3:
                pass

        self.update()

        self.memory_write(self.param_list)

    
    def minus_enable(self):
        match self.param_num:
            case 1:
                if self.param_list[self.param_num] <= 1:
                    self.button_minus.setEnabled(False)
                else:
                    self.button_minus.setEnabled(True)

            case 2:
                if self.param_list[self.param_num] <= 1:
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


    def plus(self):
        super().plus()

        self.enable_control()

        match self.param_num:
            case 1:
                if self.param_list[self.param_num] < 100:
                    self.param_list[self.param_num] += 1
                
                self.put_parametrs()
            case 2:
                if self.param_list[self.param_num] < 10:
                    self.param_list[self.param_num] += 1
                    
                self.put_parametrs()
            case 3:
                if self.param_list[self.param_num] < 2:
                    self.param_list[self.param_num] += 1

                self.put_parametrs()

            case 4:
                if self.param_list[self.param_num] < 1:
                    self.param_list[self.param_num] += 1

                self.put_parametrs()

            case 5:
                if self.param_list[self.param_num] < 1:
                    self.param_list[self.param_num] += 1

                self.put_parametrs()

        self.update()
        self.enable_control()
    

    @enable_marker_decorator('enable_marker')
    def plus_released(self):
        super().plus_released()
        self.setFocus()

        match self.param_num:
            case 1:
                pass

            case 2:
                pass

            case 3:
                pass

        self.update()

        self.memory_write(self.param_list)
        # print('pressed')


    def plus_enable(self):
        match self.param_num:
            case 1:
                if self.param_list[self.param_num] >= 100:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 2:
                if self.param_list[self.param_num] >= 10:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 3:
                if self.param_list[self.param_num] >= 2:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 4:
                if self.param_list[self.param_num] >= 1:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

            case 5:
                if self.param_list[self.param_num] >= 1:
                    self.button_plus.setEnabled(False)
                else:
                    self.button_plus.setEnabled(True)

    
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

from PyQt5.QtWidgets import QPushButton

from Filler_interface.filler import filler


from Filler_interface.Window_settings1.settings_control_copy import Control


class Control(Control):
    def __init__(self):
        super().__init__()

        self.window_name = 'robot'


    def get_parametrs(self): 
        self.param_list = {
            1: filler.param11,
            2: filler.param31,
            3: filler.param31,
        }


    def put_parametrs(self):
       filler.param11 = self.param_list[1]
       filler.param21 = self.param_list[2]
       filler.param31 = self.param_list[3]


    def default_parametrs(self):
        filler.param11 = filler.param11_def
        filler.param21 = filler.param21_def
        filler.param31 = filler.param31_def


    def set_parametrs(self):
        self.window_name = {
            1: ['Текущая статистика', 'Statistic'],
            2: ['Текущая статистика', 'Name window'],
            3: ['Общая статистика', 'Name window'],
            4: ['Общая статистика', 'Name window'],
        }   
                             
        self.param_name = {
            1: ['Скорость робота', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
            2: ['Ускорение робота', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
            3: ['Время паузы', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
        }

        self.font_size = {
            1: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            2: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            3: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
        }

        self.value_name_mini = {
            1: ['', '', '', '', ''],
            2: ['', '', '', '', ''],
            3: ['мс', 'ms', '', '', ''],
        }

        self.value_min = {
            1: 1,
            2: 1,
            3: 0,
        }

        self.value_max = {
            1: 10,
            2: 10,
            3: 9999,
        }

        self.value_id = {
            1: 0,
            2: 0,
            3: 0,
        }

        self.value_step = {
            1: 1,
            2: 1,
            3: 100,
        }

        self.value_name = {
            1: None,
            2: None,
            3: None,
        }

        self.color_text = {
            1: None,
            2: None,
            3: None,
        }


    def right_enable(self):
        if self.param_num >= len(self.param_list):
            self.button_right.setEnabled(False)
        else:
            self.button_right.setEnabled(True)


window_robot = Control()
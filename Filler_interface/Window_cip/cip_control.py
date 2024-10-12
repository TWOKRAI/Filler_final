from PyQt5.QtWidgets import QPushButton

from Filler_interface.app import app
from Filler_interface.filler import filler

from Filler_interface.Window_settings1.settings_control_copy import Control


class Control(Control):
    def __init__(self):
        super().__init__()

        self.window_name = 'cip'

        self.font_text.setPointSize(21)
        self.label_window.setFont(self.font_text)
        self.label_window.setText('ПАРАМЕТРЫ ПРОМЫВКИ')

        self.button2 = QPushButton(self)
        self.button2.setObjectName("Button_close")
        self.button2.setGeometry(0, 0, 1, 1)
        self.button2.setEnabled(False)

        self.button2.clicked.connect(self.close)


    def get_parametrs(self): 
        self.param_list = {
            1: filler.param11,
            2: filler.param21,
            3: filler.param31,
            4: filler.param41,
        }


    def put_parametrs(self):
       filler.param11 = self.param_list[1]
       filler.param21 = self.param_list[2]
       filler.param31 = self.param_list[3]
       filler.param41 = self.param_list[4]

       #print(filler.param11, filler.param21, filler.param31, filler.param41)


    def default_parametrs(self):
        filler.param11 = filler.param11_def
        filler.param21 = filler.param21_def
        filler.param31 = filler.param31_def
        filler.param41 = filler.param41_def


    def set_parametrs(self):     
        self.window_name = {
            1: ['НАСТРОЙКА ПРОМЫВКИ', 'Name window'],
            2: ['НАСТРОЙКА ПРОМЫВКИ', 'Name window'],
            3: ['НАСТРОЙКА ПРОМЫВКИ', 'Name window'],
            4: ['НАСТРОЙКА ПРОМЫВКИ', 'Name window'],
            5: ['НАСТРОЙКА ПРОМЫВКИ', 'Name window'],
            6: ['НАСТРОЙКА ПРОМЫВКИ', 'Name window'],
            7: ['НАСТРОЙКА ПРОМЫВКИ', 'Name window'],
        }   
                           
        self.param_name = {
            1: ['Насос 1: Скорость', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
            2: ['Насос 1: Состояние', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
            3: ['Насос 2: Скорость', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
            4: ['Насос 2: Состояние', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
        }

        self.font_size = {
            1: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            2: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            3: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            4: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
        }

        self.value_name_mini = {
            1: ['', '', '', '', ''],
            2: ['', '', '', '', ''],
            3: ['', '', '', '', ''],
            4: ['', '', '', '', ''],
        }

        self.value_min = {
            1: 1,
            2: None,
            3: 1,
            4: None,
        }

        self.value_max = {
            1: 5,
            2: None,
            3: 5,
            4: None,
        }

        self.value_id = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
        }

        self.value_step = {
            1: 1,
            2: [False, True],
            3: 1,
            4: [False, True],
        }

        self.value_name = {
            1: None,
            2: [['Выкл', 'Вкл'], ['No', 'Yes']],
            3: None,
            4: [['Выкл', 'Вкл'], ['No', 'Yes']],
        }

        self.color_text = {
            1: None,
            2: [None, (63, 140, 110)],
            3: None,
            4: [None, (63, 140, 110)],
        }


    def right_enable(self):
        if self.param_num >= len(self.param_list):
            self.button_right.setEnabled(False)
        else:
            self.button_right.setEnabled(True)


    def plus(self):
        super().plus()

        #print(self.param_list)

        if self.param_list[2] or self.param_list[4]:
            self.button2.setGeometry(0, 0, self.width(), self.height())
            self.button2.setEnabled(True)


    def close(self):
        self.minus()
        self.button2.setGeometry(0, 0, 1, 1)
        self.button2.setEnabled(False)


window_cip = Control()
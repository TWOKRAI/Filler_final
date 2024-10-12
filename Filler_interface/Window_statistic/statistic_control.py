from Filler_interface.filler import filler

from Filler_interface.app import app

from Filler_interface.Window_settings1.settings_template import Control


class Control(Control):
    def __init__(self):
        super().__init__()

        self.window_name = 'statistic'

        self.button_minus.hide()
        self.button_plus.hide()


    def get_parametrs(self): 
        self.param_list = {
            1: filler.static_time,
            2: filler.static_ml,
            3: filler.static_time_all,
            4: filler.static_ml_all,
        }


    def put_parametrs(self):
       filler.param11 = self.param_list[1]
       filler.param21 = self.param_list[2]
       filler.param31 = self.param_list[3]


    def default_parametrs(self):
        filler.static_time = filler.static_time_def
        filler.static_ml = filler.static_ml_def
        filler.static_time_all = filler.static_time_all_def
        filler.static_ml_all = filler.static_ml_all_def


    def set_parametrs(self):
        self.window_name = {
            1: ['ТЕКУЩАЯ СТАТИСТИКА', 'Statistic'],
            2: ['ТЕКУЩАЯ СТАТИСТИКА', 'Name window'],
            3: ['ОБЩАЯ СТАТИСТИКА', 'Name window'],
            4: ['ОБЩАЯ СТАТИСТИКА', 'Name window'],
        }   
                               
        self.param_name = {
            1: ['Время сессии', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
            2: ['Количество выпитого', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
            3: ['Общее время', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
            4: ['Общее количество выпитого', 'Volume1 /ml', 'Volumen 1 /ml', '體積 1 /毫升'],
        }

        self.font_size = {
            1: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            2: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
            3: {'window_name': 21, 'coll_params': 35, 'value': 75, 'value_mini': 30, 'name_params': 30,},
            4: {'window_name': 21, 'coll_params': 35, 'value': 90, 'value_mini': 30, 'name_params': 30,},
        }

        self.value_name_mini = {
            1: ['', '', '', '', ''],
            2: ['мл', 'ml', '', '', ''],
            3: ['', '', '', '', ''],
            4: ['мл', 'ml', '', '', ''],
        }

        self.value_min = {
            1: None,
            2: None,
            3: None,
            4: None,
        }

        self.value_max = {
            1: None,
            2: None,
            3: None,
            4: None,
        }

        self.value_id = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
        }

        self.value_step = {
            1: None,
            2: None,
            3: None,
            4: None,
        }

        self.value_name = {
            1: None,
            2: None,
            3: None,
            4: None,
        }

        self.color_text = {
            1: None,
            2: None,
            3: None,
            4: None,
        }


    def right_enable(self):
        if self.param_num >= len(self.param_list):
            self.button_right.setEnabled(False)
        else:
            self.button_right.setEnabled(True)


    def plus_enable(self):
        self.button_plus.setEnabled(False)

    
    def minus_enable(self):
        self.button_minus.setEnabled(False)


    def button_menu_clicked(self):
        app.window_list1.show()
        self.hide()


window_statistic = Control()
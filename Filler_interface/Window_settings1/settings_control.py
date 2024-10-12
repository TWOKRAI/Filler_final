from Filler_interface.app import app

from Filler_interface.Window_settings1.settings_control_copy import Control


from Filler_interface.filler import filler


class Control(Control):
    def __init__(self):
        super().__init__()


    def put_parametrs(self):
       filler.param1 = self.param_list[1]
       filler.param2 = self.param_list[2]
       filler.param3 = self.param_list[3]
       filler.param4 = self.param_list[4]
       filler.param5 = self.param_list[5]
       filler.param6 = self.param_list[6]

    #    print(filler.param1, filler.param2, filler.param3, filler.param4)

    
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
            1: ['НАСТРОЙКА НАЛИВА', 'Name window'],
            2: ['НАСТРОЙКА НАЛИВА', 'Name window'],
            3: ['НАСТРОЙКА НАЛИВА', 'Name window'],
            4: ['НАСТРОЙКА НАЛИВА', 'Name window'],
            5: ['НАСТРОЙКА НАЛИВА', 'Name window'],
            6: ['НАСТРОЙКА НАЛИВА', 'Name window'],
            7: ['НАСТРОЙКА НАЛИВА', 'Name window'],
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
            7: [['Готово'], ['Ready']],
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
    
    
    def button_menu_clicked(self):
        app.window_list1.show()
        self.hide()


    def right(self):
        if self.param_num == 7:
            app.window_prepare.show()
            self.hide()    

        super().right()


window_setting = Control()
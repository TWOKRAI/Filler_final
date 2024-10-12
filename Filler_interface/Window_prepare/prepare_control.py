from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QSize, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import os

from Filler_interface.app import app, enable_marker_decorator


class Prepare_control(QMainWindow):
    calibration = pyqtSignal()
    reset_calibration = pyqtSignal()
    find_cup = pyqtSignal()
    pumping = pyqtSignal()
    stop_pumping = pyqtSignal()
    start_filler = pyqtSignal()

    def __init__(self):
        super().__init__()

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface/Window_prepare', 'UI_prepare.ui')
        # file_path = os.path.join('Filler_interface', 'Window_prepare', 'UI_prepare.ui')
        uic.loadUi(file_path, self)

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.window_name = 'prepare'

        icon_size = QSize(65, 65)
        button_size_1 = QSize(140, 130)
        button_size_2 = QSize(210, 130)

        font_1 = QFont()
        font_1.setFamily(app.font_family)
        font_1.setPointSize(25)
        font_1.setBold(False)
        font_1.setWeight(50)

        font_2 = QFont()
        font_2.setFamily(app.font_family)
        font_2.setPointSize(18)
        font_2.setBold(False)
        font_2.setWeight(50)

        self.label.setFont(font_1)
        self.label.setWordWrap(True)

        self.button_menu.setIconSize(icon_size)
        self.button_menu.setFixedSize(button_size_1)
        self.button_reset.setIconSize(icon_size)
        self.button_reset.setFixedSize(button_size_1)

        self.set_icons()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(1000) 
        self.timer.timeout.connect(self.on_timer_timeout)

        self.button_menu.clicked.connect(self.button_menu_clicked)
        self.button_menu.pressed.connect(self.button_menu_pressed)
        self.button_menu.released.connect(self.button_menu_released)

        self.button_reset.released.connect(self.show_popup)

        self.button_calibr.released.connect(self.button_calibr_clicked)
        self.button_calibr.setFont(font_2)
        self.button_calibr.setFixedSize(button_size_2)

        self.sort_button = False

        self.myprogressBar.setMinimum(0)
        self.myprogressBar.setMaximum(100) 

        self.value = 0
        self.myprogressBar.setValue(self.value)
      
        self.param_num = 0
        self.lang = 0

        self.update()

        self.timer_enable = QTimer(self)
        self.timer_enable.setSingleShot(True) 
        self.timer_enable.timeout.connect(self.all_enable_on)
        self.timer_enable.start(1000) 
        self.enable_marker = True


    def show(self):
        if app.on_fullscreen: self.fullscreen()

        super().show()

        self.update_text()

        app.window_focus = self.window_name
        #app.close_windows()

        self.setFocus()

        self.all_enable_off()

        # app.threads.start_robot_thread(camera_on = True, neuron_on = True, interface_on = True, robot_on = True)


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def language(self, lang):
        self.lang = lang

        self.update_text()


    def set_icons(self):
        self.button_reset_update()
        self.button_menu_update()
        
    
    def update_text(self):
        self.button_calibr_update()
        self.label_update()


    def all_enable_on(self):
        self.enable_marker = True

    
    def all_enable_off(self):
        self.enable_marker = False
        self.timer_enable.start()


    @enable_marker_decorator('enable_marker')
    def show_popup(self):
        app.window_pop_up.hide()
        app.window_pop_up.show(self.reset)

        pop_show_text = {
            0: 'Вы хотите начать калибровку заново?',
            1: 'Do you want to start calibration again?',
            2: 'Möchten Sie die Kalibrierung erneut starten?',
        }

        app.window_pop_up.label_2.setText(pop_show_text[self.lang])

    
    def button_reset_update(self):
        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-replay-100.png')
        self.button_reset.setIcon(QIcon(file_path))


    def reset(self):
        self.param_num = 0
        
        self.value = 0
        self.myprogressBar.setValue(self.value)
        self.button_calibr.setEnabled(True)

        self.reset_calibration.emit()

        self.update_text()
        

    def button_menu_update(self):
        icon_size = QSize(75, 75)
        self.button_menu.setIconSize(icon_size)

        button_size = QSize(140, 130)
        self.button_menu.setFixedSize(button_size)

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-закрыть-окно-96')
        self.button_menu.setIcon(QIcon(file_path))


    def button_menu_clicked(self):
        pass

    
    @enable_marker_decorator('enable_marker')
    def button_menu_pressed(self):
        self.timer.start()


    @enable_marker_decorator('enable_marker')
    def button_menu_released(self):
        if  app.threads.robot_filler.pumping_ready != True:
            self.reset()

        self.setFocus()
        app.window_main_filler.show()
        self.hide()

        self.timer.stop()
 
        
    def on_timer_timeout(self):
        app.window_main_filler.show()
        self.hide()
    

    def button_calibr_update(self):
        match self.param_num:
            case 0:
                name_button = {
                    0: 'КАЛИБРОВКА',
                    1: 'CALIBRATION',
                    2: 'KALIBRIERUNG',
                }

            case 1:
                name_button = {
                    0: 'ПОДОЖДИТЕ',
                    1: 'WAIT',
                    2: 'WARTEN'
                }


            case 2:
                name_button = {
                    0: 'ПОДОЖДИТЕ',
                    1: 'WAIT',
                    2: 'WARTEN'
                }


            case 3:
                name_button = {
                    0: 'ПОДОЖДИТЕ',
                    1: 'WAIT',
                    2: 'WARTEN'
                }

  
            case 4:
                name_button = {
                    0: 'ПОДОЖДИТЕ',
                    1: 'WAIT',
                    2: 'WARTEN'
                }


            case 6:
                name_button = {
                    0: 'НАЧАТЬ',
                    1: 'START',
                    2: 'STARTEN',
                }


            case _:
                name_button = {
                    0: 'НАЧАТЬ',
                    1: 'START',
                    2: 'STARTEN',
                }
        
        self.button_calibr.setText(name_button[self.lang])

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(23)
        font.setBold(False)
        font.setWeight(50)
        self.button_calibr.setFont(font)

        button_size = QSize(200, 130)
        self.button_calibr.setFixedSize(button_size)
        

    def button_calibr_enable(self):
        pass 

    
    @enable_marker_decorator('enable_marker')
    def button_calibr_clicked(self):
        self.param_num += 1

        if self.param_num >= 6:
            self.param_num = 6

        # print('self.param_num', self.param_num)

        if app.threads.robot_filler.pumping_ready == True:
            self.param_num = 6
            #app.threads.robot_filler.pumping_ready = False

        match self.param_num:
            case 1:
                app.threads.robot_filler.calibration_run()

                self.value = 25

                self.button_calibr.setEnabled(False)
            
            case 2:                
                self.value = 50

            case 3:
                self.value = 70

            case 4:
                self.value = 90
        
            case 5:
                self.value = 100

                app.threads.robot_filler.calibration_stop()

            case 6:
                # app.threads.robot_filler.filler_run()

                app.threads.robot_filler.pumping_ready = True

                app.window_filler.show()
                self.hide()
                # self.param_num = 0

            case _:
                pass
        

        self.label_update()
        self.button_calibr_update()

        self.myprogressBar.setValue(self.value)


    def label_update(self):
        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)

        self.label.setFont(font)
        self.label.setWordWrap(True)

        match self.param_num:
            case 0:
                label_name = {
                    0: 'Поставьте стакан перед роботом и нажмите "КАЛИБРОВКА"',
                    1: 'Place the glass in front of the robot and press "CALIBRATION"',
                    2: 'Platzieren Sie das Glas vor dem Roboter und drücken Sie „KALIBRIERUNG“.'
                }

            case 1:
                label_name = {
                    0: 'Началась калибровка робота',
                    1: 'Robot calibration has begun',
                    2: 'Die Roboterkalibrierung hat begonnen',
                }


            case 2:
                label_name = {
                    0: 'Поставьте стакан в рабочую зону для прокачки системы',
                    1: 'Place the glass in the work area to bleed the system',
                    2: 'Stellen Sie ein Glas in den Arbeitsbereich, um das System zu entlüften',
                }
                                
   

            case 3:
                label_name = {
                    0: 'Стакан обнаружен, началась прокачка системы',
                    1: 'Glass detected, system bleeding started',
                    2: 'Das Glas wurde erkannt, das System hat mit dem Pumpen begonnen'
                }


            case 4:
                label_name = {
                    0: 'Прокачка системы закончена',
                    1: 'System pumping is complete',
                    2: 'Die Systementlüftung ist abgeschlossen'
                }
                                

                self.value = 90

            case 5:
                label_name = {
                    0: 'Система готова',
                    1: 'The system is ready',
                    2: 'System bereit'
                }

                self.label.setText(label_name[self.lang])
                self.button_calibr.setEnabled(True)

                self.label.setText(label_name[self.lang])

                self.value = 100
            case 6:
                label_name = {
                    0: 'Система готова',
                    1: 'The system is ready',
                    2: 'System bereit'
                }

                self.label.setText(label_name[self.lang])
                self.button_calibr.setEnabled(True)

                self.label.setText(label_name[self.lang])

                self.value = 100

            case 7:
                label_name = {
                    0: 'Система готова',
                    1: 'The system is ready',
                    2: 'System bereit'
                }

                self.label.setText(label_name[self.lang])
                self.button_calibr.setEnabled(True)

                self.label.setText(label_name[self.lang])

                self.value = 100


        self.label.setText(label_name[self.lang])

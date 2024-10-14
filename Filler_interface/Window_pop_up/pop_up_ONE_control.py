from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import os

from Filler_interface.app import app


class Confirm_control(QMainWindow):
    def __init__(self):
        super().__init__()

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface/Window_pop_up', 'UI_confirm.ui')
        # file_path = os.path.join('Filler_interface', 'Window_pop_up', 'UI_pop_up.ui')
        uic.loadUi(file_path, self)
       
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.window_name = 'pop_confirm'

        self.func = None
        self.func_cancel = None

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(500) 
        self.timer.timeout.connect(self.hide)


        self.font_text = QFont()
        self.font_text.setFamily(app.font_family)

        font_1 = QFont()
        font_1.setFamily(app.font_family)
        font_1.setPointSize(55)
        font_1.setBold(False)
        font_1.setWeight(50)

        font_2 = QFont()
        font_2.setFamily(app.font_family)
        font_2.setPointSize(30)
        font_2.setBold(False)
        font_2.setWeight(50)

        self.label_2.setFont(font_1)
        self.label_2.setFixedSize(300, 100) 
        self.label_2.setWordWrap(True)
        self.label_2.setScaledContents(True)

        self.label_2.setMinimumSize(600, 120) 

        self.pushButton_ok.setFixedSize(180, 140)
        self.pushButton_ok.setFont(font_2)

        self.pushButton_ok.released.connect(self.ok)

        self.pushButton_cancel.setFixedSize(180, 140)
        self.pushButton_cancel.setFont(font_2)

        self.pushButton_cancel.released.connect(self.cancel)
        self.pushButton_cancel.hide()


        self.lang = 0

        self.text = [
            'Для того чтобы выполнить прокачку системы, поставьте стакан в рабочую зону и нажмите "ПРОДОЛЖИТЬ".', 
            'To perform the system calibration, place the glass in the work area and press "CONTINUE".',
            'Um das System zu kalibrieren, stellen Sie das Glas in den Arbeitsbereich und drücken Sie "WEITER".', 
        ]

        self.text_button_ok = [
            'ПРОДОЛЖИТЬ', 
            'CONTINUE',
            'WEITER', 
        ]

        self.text_button_cancel = [
            'ОТМЕНИТЬ', 
            'CANCEL',
            'STORNIEREN', 
        ]

        self.font_size = [
            [29, 21],
            [29, 21],
            [29, 21],
            [29, 21],
        ]


    def show(self, func):
        if app.on_fullscreen: self.fullscreen()

        self.update_text()
        self.func = func

        super().show()
        
        self.setFocus()

    
    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def language(self, lang):
        self.lang = lang

        self.update_text()


    def update_text(self):
        size = self.font_size[self.lang][0]
        self.font_text.setPointSize(size)
        self.label_2.setFont(self.font_text)
        self.label_2.setText(self.text[app.lang_num])

        size = self.font_size[self.lang][1]
        self.font_text.setPointSize(size)
        self.pushButton_ok.setFont(self.font_text)
        self.pushButton_ok.setText(self.text_button_ok[app.lang_num])

        size = self.font_size[self.lang][1]
        self.font_text.setPointSize(size)
        self.pushButton_cancel.setFont(self.font_text)
        self.pushButton_cancel.setText(self.text_button_cancel[self.lang])


    def ok(self):
        self.func()
        self.timer.start()

        self.setFocus()
        
    
    def cancel(self):
        if self.func_cancel != None:
            self.func_cancel()
            self.func_cancel = None
        
        self.setFocus()
        self.hide()
        

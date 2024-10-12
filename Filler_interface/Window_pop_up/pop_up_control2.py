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

        # self.setStyleSheet("""
        #     QWidget{
        #         border: 3px solid rgb(108, 161, 141);
        #     }
            
        #     QLabel{
        #         border: 0px solid rgb(108, 161, 141);        
        #     }
                           
        #     QPushButton {
        #         background-color: #dad7d7;
        #         background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
        #         stop: 0 white, stop: 0.7 #A9A9A9, stop: 0.95 #dad7d7);
        #         border-radius: 25px;
        #         color: rgb(63, 94, 83);
        #         border: 4px solid rgb(108, 161, 141);
        #         border-bottom: 5px solid rgb(87, 121, 101);
        #     }

        #     QPushButton:hover {
        #         background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, 
        #         stop: 0 white, stop: 0.7 #A9A9A9, stop: 0.95 #dad7d7);
        #         border: 4px solid rgb(108, 161, 141);
        #     }

        #     QPushButton#Button_close {
        #         background-color: rgba(0, 0, 0, 0);
        #         border: none;
        #     }
        # """)

        self.lang = 0

        self.text = [
            'Вы хотите сделать сброс параметров?', 
            'Do you want to reset the parameters?',
            'Möchten Sie Ihre Einstellungen zurücksetzen?', 
        ]

        self.text_button_ok = [
            'ПОДТВЕРДИТЬ', 
            'CONFIRM',
            'BESTÄTIGEN', 
        ]

        self.text_button_cancel = [
            'ОТМЕНИТЬ', 
            'CANCEL',
            'STORNIEREN', 
        ]

        self.font_size = [
            [33, 21],
            [33, 21],
            [33, 21],
            [33, 21],
        ]


    def show(self, func):
        if app.on_fullscreen: self.fullscreen()

        # app.window_focus = self.window_name
        # print(app.window_focus)

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
        self.label_2.setText(self.text[self.lang])

        size = self.font_size[self.lang][1]
        self.font_text.setPointSize(size)
        self.pushButton_ok.setFont(self.font_text)
        self.pushButton_ok.setText(self.text_button_ok[self.lang])

        size = self.font_size[self.lang][1]
        self.font_text.setPointSize(size)
        self.pushButton_cancel.setFont(self.font_text)
        self.pushButton_cancel.setText(self.text_button_cancel[self.lang])


    def ok(self):
        self.func()
        self.timer.start()

        self.setFocus()
        
    
    def cancel(self):
        self.hide()

        self.setFocus()
        

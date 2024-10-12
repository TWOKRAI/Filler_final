from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QFont

import datetime
import os

from Filler_interface.app import app


class Datetime_control(QMainWindow):
    def __init__(self):
        super().__init__()

        self.window_name = 'datetime'

        # file_path = os.path.join('Filler','Filler_interface', 'Window_datetime', 'UI_datetime.ui')
        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface/Window_datetime', 'UI_datetime.ui')
        uic.loadUi(file_path, self)
        

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.update_time()

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', '1x', 'innotech_min.png')
        pixmap = QPixmap(file_path)
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.5), int(pixmap.height() * 0.5), Qt.KeepAspectRatio)
        self.innotech_min.setPixmap(scaled_pixmap)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        #self.timer.start(1000)


        #self.animation = QPropertyAnimation(self, b'windowOpacity')
        
        # self.opacity_effect = QGraphicsOpacityEffect(self)
        # self.opacity_effect.setOpacity(0.0)  # Начальная прозрачность (полностью прозрачно)
        # self.setGraphicsEffect(self.opacity_effect)

        # self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")

        font_1 = QFont()
        font_1.setFamily(app.font_family)
        font_1.setPointSize(133)
        font_1.setBold(False)

        self.time_text.setFont(font_1)

        font_2 = QFont()
        font_2.setFamily(app.font_family)
        font_2.setPointSize(40)
        font_2.setBold(False)

        self.date.setFont(font_2)


    def timing(self):
        self.timer.stop()


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()
        self.button_raise()
        super().show()


    def show_window(self):
        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
        'background-color: None',
        'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.5 #DCDCDC, stop: 0.9 #949494);'
        )
        
        app.setStyleSheet(new_stylesheet)
    
        self.timer.stop()
        self.timer.start(1000)

        #self.setWindowOpacity(0.0)  
        self.show()  
        #self.start_animation()     


    def button_raise(self):
        self.button = QPushButton(self)
        self.button.setObjectName("Button_close")
        self.button.setGeometry(0, 0, self.width(), self.height())
        self.button.raise_()

        self.button.clicked.connect(self.close)


    def start_animation(self):
        pass
        # self.animation.stop()
        # self.animation.setDuration(3000)  
        # self.animation.setStartValue(0.0)  
        # self.animation.setEndValue(1.0)
        # self.animation.start()
    

    def close(self):
        self.timer.stop()

        app.datetime_reset()
        self.hide()


    def update_time(self):
        now = datetime.datetime.now()
        time = now.strftime("%H:%M")
        date = now.strftime("%d/%m/%Y")
        self.time_text.setText(time)
        self.date.setText(date)
    
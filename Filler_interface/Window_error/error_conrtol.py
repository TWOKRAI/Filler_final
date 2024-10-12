from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QSize
from PyQt5.QtGui import QFont, QPixmap, QMovie
import os 

from Filler_interface.app import app

try:
    raspberry = True
except ImportError:
    raspberry = False


class Error_control(QMainWindow):
    def __init__(self):
        super().__init__()

        
        # file_path = os.path.join('Filler_interface', 'Window_error', 'UI_error.ui')

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface/Window_error', 'UI_error.ui')
        uic.loadUi(file_path, self)

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.window_name = 'error'

        # if raspberry:
        #     input_request.show_error.connect(self.show)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.start_time = 5000


        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', '1x', 'innotech_min.png')
        pixmap = QPixmap(file_path)
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.5), int(pixmap.height() * 0.5), Qt.KeepAspectRatio)
        self.innotech_min.setPixmap(scaled_pixmap)

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_no_color', 'error.png')
        pixmap = QPixmap(file_path)
        scaled_pixmap = pixmap.scaled(int(pixmap.width()* 0.8), int(pixmap.height()* 0.8), Qt.KeepAspectRatio)
        self.level_img.setPixmap(scaled_pixmap)


        self.button = QPushButton(self)
        self.button.setObjectName("Button_close")
        self.button.setGeometry(0, 0, self.width(), self.height())
        self.button.raise_()

        self.animation = QPropertyAnimation(self, b'windowOpacity')

        self.button.clicked.connect(self.close)

        self.lang = 0
        self.code = 0

        self.update()


    def timing(self):
        self.timer.stop()


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()
        super().show()

        self.update()


    def close(self):
        # if not input_request.button_error:
        self.hide()


    def language(self, lang):
        self.lang = lang

        self.update()


    def update(self):
        self.label_update()


    def label_update(self):
        match self.code:
            case 0:
                label_name = {
                    0: 'Нажата авайрийная кнопка',
                    1: 'Emergency button pressed',
                    2: 'Not-Aus-Taste gedrückt',
                }
            case _:
                label_name = {
                    0: '',
                    1: '',
                }

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(33)
        font.setBold(False)
        font.setWeight(50)
        self.label_warning.setFont(font)
        self.label_warning.setWordWrap(False)

        self.label_warning.setText(label_name[self.lang])

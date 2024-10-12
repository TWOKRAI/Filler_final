from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget
from Filler_interface.Window_low.main_low import Ui_low
from PyQt5.QtCore import Qt

from Filler_interface.app import app 


class Low_control(QMainWindow, Ui_low):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)

        self.setupUi(self)
        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.button = QPushButton(self)
        self.button.setObjectName("Button_close")
        self.button.setGeometry(0, 0, self.width(), self.height())
        self.button.raise_()

        self.button.released.connect(self.close)

    
    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()
        #super().show()

    
    def close(self):
        app.close_windows()
        app.show_windows()

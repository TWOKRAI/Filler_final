from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QTimer
from Filler_interface.Window_qrcode.qrcode import Ui_MainWindow

from Filler_interface.app import app


class QRCodeControl(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        font = QtGui.QFont()
        font.setPointSize(25)
        font.setFamily(app.font_family)
        self.label_login.setFont(font)
        self.label_password.setFont(font)
        self.label_ip_address.setFont(font)
        self.label_ip.setFont(font)
        
        self.button_raise()

        self.timer_enable = QTimer(self)    
        self.timer_enable.setSingleShot(True)  
        self.timer_enable.timeout.connect(self.enable_on)
        self.enable_marker = False



    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def enable_on(self):
        self.enable_marker = True


    def show(self):
        if app.on_fullscreen: self.fullscreen()
        if not self.isVisible():
            super().show()
            self.button_raise()
        else:
            self.hide()
            super().show()
            self.button_raise()
        
        self.enable_marker = False
        self.timer_enable.start(1000)
            

    def close(self):
        if self.enable_marker:
            self.hide()

    
    def button_raise(self):
        self.button = QtWidgets.QPushButton(self)
        self.button.setObjectName("Button_close")
        self.button.setGeometry(0, 0, self.width(), self.height())
        self.button.raise_()

        self.button.clicked.connect(self.close)
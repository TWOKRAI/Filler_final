from PyQt5 import QtWidgets
from Filler_interface.Window_qrcode.qrcode import Ui_MainWindow


class QRCodeControl(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


    def show(self):
        super().show()
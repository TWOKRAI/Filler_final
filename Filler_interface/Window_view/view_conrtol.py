from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPixmap
import os
import numpy as np
# from PIL import Image
# import io


from Filler_interface.app import app


class View_control(QMainWindow):
    view_start = pyqtSignal()
    view_stop = pyqtSignal()

    def __init__(self):
        super().__init__()

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface/Window_view', 'UI_view.ui')

        # file_path = os.path.join('Filler_interface', 'Window_view', 'UI_view.ui')
        uic.loadUi(file_path, self)

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.window_name = 'view'

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', '1x', 'innotech_min.png')
        pixmap = QPixmap(file_path)
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.5), int(pixmap.height() * 0.5), Qt.KeepAspectRatio)
        self.innotech_min.setPixmap(scaled_pixmap)

        self.image_low()
        self.button_raise()

        self.focus_window = False

        self.frame_label = None

        self.view2 = False


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self, id = 0):
        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
            'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.4 #DCDCDC, stop: 0.9 #878787);',
            'background-color: None'
        )
        
        app.setStyleSheet(new_stylesheet)
    
        self.hide()

        if app.window_filler.play == False:
            #app.threads.robot_filler.view_run() 
            self.view_start.emit()
        else:
            pass


        # if id == 1:
        #     self.view2 = True
        #     app.threads.robot_filler.view_run()   
        # else:
        #     self.view2 = False
                 

        if app.on_fullscreen: self.fullscreen()

        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
        'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.4 #DCDCDC, stop: 0.9 #878787);',
        'background-color: None'
        )
        
        app.setStyleSheet(new_stylesheet)

        self.focus_window = True

        super().show()


    def close(self):
        self.view_stop.emit()

        stylesheet = app.styleSheet()
        new_stylesheet = stylesheet.replace(
        'background-color: None',
        'background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 white, stop: 0.4 #DCDCDC, stop: 0.9 #878787);'
        )
        
        app.setStyleSheet(new_stylesheet)

        self.focus_window = False

        self.hide()


    def button_raise(self):
        self.button = QPushButton(self)
        self.button.setObjectName("Button_close")
        self.button.setGeometry(0, 0, self.width(), self.height())
        self.button.raise_()

        self.button.clicked.connect(self.close)
    

    def image_low(self):
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.width(), self.height())
        # file_path = os.path.join('Filler_interface', 'Window_view', 'images.png')
        # self.label.setPixmap(QPixmap(file_path))
        self.label.setScaledContents(True)
        self.label.lower()


    @pyqtSlot(QPixmap)
    def update_frame(self, frame):
        self.label.setPixmap(frame)

        if self.focus_window:
            app.datetime_reset()


    # @pyqtSlot(np.ndarray)
    # def update_image(self, array):
    #     image = Image.fromarray(array)
    #     buffer = io.BytesIO()
    #     image.save(buffer, format="JPEG")
    #     qimage = QPixmap()
    #     qimage.loadFromData(buffer.getvalue())
    #     self.label.setPixmap(qimage)

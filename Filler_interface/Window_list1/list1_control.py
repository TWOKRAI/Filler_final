from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation
from PyQt5.QtGui import QIcon, QFont
import os

from Filler_interface.app import app


class List_control(QMainWindow):
    def __init__(self):
        super().__init__()

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface/Window_list1', 'UI.ui')
        # file_path = os.path.join('Filler_interface', 'Window_list1', 'UI.ui')
        uic.loadUi(file_path, self)

        self.statusBar().setHidden(True)
        self.setFixedSize(app.window_size)

        self.window_name = 'list1'

        self.timer = QTimer()
        self.timer.timeout.connect(self.datetime)
        
        icon_size = QSize(55, 55)
        icon_size_2 = QSize(65, 65)
        button_size = QSize(210, 130)
        button_size_2 = QSize(130, 130)

        font = QFont()
        font.setFamily(app.font_family)
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)


        self.button_menu.setMinimumSize(button_size_2)
        self.button_menu.setIconSize(icon_size_2)

        self.button_menu.clicked.connect(self.button_menu_clicked)


        self.start_text = [' ВИД', ' VISION', ' VISION']
        
        self.button_view.setMinimumSize(button_size)
        self.button_view.setIconSize(icon_size)
        self.button_view.setFont(font)

        self.button_view.clicked.connect(self.view)


        self.game_text = [' НАСТРОЙКИ', ' SETTINGS', 'EINSTELLUNGEN']
        
        self.button_game.setMinimumSize(button_size)
        self.button_game.setIconSize(icon_size)
        self.button_game.setFont(font)

        self.button_game.clicked.connect(self.settings)


        self.statistics_text = [' QR-KОД', ' QR-СODE', ' QR-СODE']
        
        self.button_qrcode.setMinimumSize(button_size)
        self.button_qrcode.setIconSize(icon_size)
        self.button_qrcode.setFont(font)

        self.button_qrcode.clicked.connect(self.statistics)

        self.animation = QPropertyAnimation(self, b'windowOpacity')

        self.set_icons()


    def fullscreen(self):        
        self.setWindowState(Qt.WindowFullScreen)


    def show(self):
        if app.on_fullscreen: self.fullscreen()

        #self.language(app.lang)
        super().show()
        
        app.window_focus = self.window_name
        app.close_windows()


    def set_icons(self):
        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-закрыть-окно-96')
        self.button_menu.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-preview-pane-100.png')
        self.button_view.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-automation-100.png')
        self.button_game.setIcon(QIcon(file_path))

        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface', 'Style_windows', 'icons_black', 'icons8-qr-code-96.png')
        self.button_qrcode.setIcon(QIcon(file_path))


    def language(self, lang):
        self.button_view.setText(self.start_text[lang])
        self.button_game.setText(self.game_text[lang])
        self.button_qrcode.setText(self.statistics_text[lang])
    

    def button_menu_clicked(self):
        self.hide()


    def view(self):
        app.window_view.show()

    
    def datetime(self):
        app.window_datetime.show_window()
        self.timer.stop()


    def settings(self):
        app.window_settings2.show()
        # self.hide()

    
    def statistics(self):
        app.window_statistic.show()
        self.hide()
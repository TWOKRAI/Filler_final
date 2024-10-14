from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self.verticalLayout.setObjectName("verticalLayout")

        # Верхняя строка для картинки в правом верхнем углу
        self.horizontalLayout_top = QtWidgets.QHBoxLayout()
        self.horizontalLayout_top.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self.horizontalLayout_top.setObjectName("horizontalLayout_top")

        spacerItem_top_left = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_top.addItem(spacerItem_top_left)

        self.image_top = QtWidgets.QLabel(self.centralwidget)
        self.image_top.setMinimumSize(QtCore.QSize(395, 85))
        self.image_top.setMaximumSize(QtCore.QSize(395, 85))

        # Обрезаем изображение сверху на 15 пикселей
        pixmap = QtGui.QPixmap("/home/innotech/Project/Filler/Filler_interface/1x/innotech_min.png")
        cropped_pixmap = pixmap.copy(0, 15, pixmap.width(), pixmap.height() - 15)
        self.image_top.setPixmap(cropped_pixmap)

        self.image_top.setScaledContents(True)
        self.image_top.setObjectName("image_top")
        self.horizontalLayout_top.addWidget(self.image_top)

        self.verticalLayout.addLayout(self.horizontalLayout_top)

        # Горизонтальный layout для картинок и надписей
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self.gridLayout.setObjectName("gridLayout")

        # Добавляем пространство слева и справа от картинок
        spacerItem_left = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem_right = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem_left, 0, 0)
        self.gridLayout.addItem(spacerItem_right, 0, 4)

        # Первая картинка и текст под ней
        self.image1 = QtWidgets.QLabel(self.centralwidget)
        self.image1.setMinimumSize(QtCore.QSize(250, 250))  # Увеличиваем размер в полтора раза
        self.image1.setMaximumSize(QtCore.QSize(250, 250))
        self.image1.setPixmap(QtGui.QPixmap("/home/innotech/Project/Filler_final/Server2/qr_code_module/wifi_qr_code.png"))
        self.image1.setScaledContents(True)
        self.image1.setObjectName("image1")
        self.gridLayout.addWidget(self.image1, 0, 1, QtCore.Qt.AlignCenter)

        # Вертикальный layout для текста под первой картинкой
        self.verticalLayout_text1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_text1.setSpacing(5)  # Уменьшаем расстояние между строчками текста

        # Добавляем пространство перед текстом
        spacerItem_text1 = QtWidgets.QSpacerItem(55, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)  # Уменьшаем высоту
        self.verticalLayout_text1.addItem(spacerItem_text1)

        self.label_login = QtWidgets.QLabel(self.centralwidget)
        self.label_login.setAlignment(QtCore.Qt.AlignCenter)
        self.label_login.setObjectName("label_login")
        self.verticalLayout_text1.addWidget(self.label_login)

        self.label_password = QtWidgets.QLabel(self.centralwidget)
        self.label_password.setAlignment(QtCore.Qt.AlignCenter)
        self.label_password.setObjectName("label_password")
        self.verticalLayout_text1.addWidget(self.label_password)

        # Добавляем пространство снизу текста
        spacerItem_text1_bottom = QtWidgets.QSpacerItem(55, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)  # Добавляем отступ снизу
        self.verticalLayout_text1.addItem(spacerItem_text1_bottom)

        self.gridLayout.addLayout(self.verticalLayout_text1, 1, 1, QtCore.Qt.AlignCenter)

        # Вторая картинка и текст под ней
        self.image2 = QtWidgets.QLabel(self.centralwidget)
        self.image2.setMinimumSize(QtCore.QSize(250, 250))  # Увеличиваем размер в полтора раза
        self.image2.setMaximumSize(QtCore.QSize(250, 250))
        self.image2.setPixmap(QtGui.QPixmap("/home/innotech/Project/Filler_final/Server2/qr_code_module/django_qr_code.png"))
        self.image2.setScaledContents(True)
        self.image2.setObjectName("image2")
        self.gridLayout.addWidget(self.image2, 0, 3, QtCore.Qt.AlignCenter)

        # Вертикальный layout для текста под второй картинкой
        self.verticalLayout_text2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_text2.setSpacing(5)  # Уменьшаем расстояние между строчками текста

        # Добавляем пространство перед текстом
        spacerItem_text2 = QtWidgets.QSpacerItem(55, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)  # Уменьшаем высоту
        self.verticalLayout_text2.addItem(spacerItem_text2)

        self.label_ip_address = QtWidgets.QLabel(self.centralwidget)
        self.label_ip_address.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ip_address.setObjectName("label_ip_address")
        self.verticalLayout_text2.addWidget(self.label_ip_address)

        self.label_ip = QtWidgets.QLabel(self.centralwidget)
        self.label_ip.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ip.setObjectName("label_ip")
        self.verticalLayout_text2.addWidget(self.label_ip)

        # Добавляем пространство снизу текста
        spacerItem_text2_bottom = QtWidgets.QSpacerItem(55, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)  # Добавляем отступ снизу
        self.verticalLayout_text2.addItem(spacerItem_text2_bottom)

        self.gridLayout.addLayout(self.verticalLayout_text2, 1, 3, QtCore.Qt.AlignCenter)

        # Добавляем пространство между картинками
        spacerItem_middle = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem_middle, 0, 2)

        self.verticalLayout.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Устанавливаем стили для отображения границ виджетов
        #self.set_debug_styles()

    def set_debug_styles(self):
        # Устанавливаем стили для отображения границ виджетов
        self.centralwidget.setStyleSheet("QWidget { border: 1px solid red; }")
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_top.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_text1.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_text2.setContentsMargins(1, 1, 1, 1)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_login.setText(_translate("MainWindow", "1. WIFI:"))
        self.label_password.setText(_translate("MainWindow", "SSID: Keenetic-6348"))
        self.label_ip_address.setText(_translate("MainWindow", "2. IP-Address:"))
        self.label_ip.setText(_translate("MainWindow", "192.168.1.108"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

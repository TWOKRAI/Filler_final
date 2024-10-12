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
        self.image_top.setMinimumSize(QtCore.QSize(200, 100))  # Увеличиваем размер в два раза по горизонтали
        self.image_top.setMaximumSize(QtCore.QSize(200, 100))
        self.image_top.setPixmap(QtGui.QPixmap("/home/innotech/Project/Filler/Filler_interface/1x/innotech_min.png"))
        self.image_top.setScaledContents(True)
        self.image_top.setObjectName("image_top")
        self.horizontalLayout_top.addWidget(self.image_top)

        self.verticalLayout.addLayout(self.horizontalLayout_top)

        # Горизонтальный layout для картинок и надписей
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self.gridLayout.setObjectName("gridLayout")

        # Первая картинка и текст под ней
        self.image1 = QtWidgets.QLabel(self.centralwidget)
        self.image1.setMinimumSize(QtCore.QSize(225, 225))  # Увеличиваем размер в полтора раза
        self.image1.setMaximumSize(QtCore.QSize(225, 225))
        self.image1.setPixmap(QtGui.QPixmap("/home/innotech/Project/Filler_final/Server2/qr_code_module/django_qr_code.png"))
        self.image1.setScaledContents(True)
        self.image1.setObjectName("image1")
        self.gridLayout.addWidget(self.image1, 0, 0, QtCore.Qt.AlignCenter)

        self.label_wifi = QtWidgets.QLabel(self.centralwidget)
        self.label_wifi.setAlignment(QtCore.Qt.AlignCenter)
        self.label_wifi.setObjectName("label_wifi")
        self.gridLayout.addWidget(self.label_wifi, 1, 0, QtCore.Qt.AlignCenter)

        self.label_login = QtWidgets.QLabel(self.centralwidget)
        self.label_login.setAlignment(QtCore.Qt.AlignCenter)
        self.label_login.setObjectName("label_login")
        self.gridLayout.addWidget(self.label_login, 2, 0, QtCore.Qt.AlignCenter)

        self.label_password = QtWidgets.QLabel(self.centralwidget)
        self.label_password.setAlignment(QtCore.Qt.AlignCenter)
        self.label_password.setObjectName("label_password")
        self.gridLayout.addWidget(self.label_password, 3, 0, QtCore.Qt.AlignCenter)

        # Вторая картинка и текст под ней
        self.image2 = QtWidgets.QLabel(self.centralwidget)
        self.image2.setMinimumSize(QtCore.QSize(225, 225))  # Увеличиваем размер в полтора раза
        self.image2.setMaximumSize(QtCore.QSize(225, 225))
        self.image2.setPixmap(QtGui.QPixmap("/home/innotech/Project/Filler_final/Server2/qr_code_module/wifi_qr_code.png"))
        self.image2.setScaledContents(True)
        self.image2.setObjectName("image2")
        self.gridLayout.addWidget(self.image2, 0, 1, QtCore.Qt.AlignCenter)

        self.label_ip_address = QtWidgets.QLabel(self.centralwidget)
        self.label_ip_address.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ip_address.setObjectName("label_ip_address")
        self.gridLayout.addWidget(self.label_ip_address, 1, 1, QtCore.Qt.AlignCenter)

        self.label_ip = QtWidgets.QLabel(self.centralwidget)
        self.label_ip.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ip.setObjectName("label_ip")
        self.gridLayout.addWidget(self.label_ip, 2, 1, QtCore.Qt.AlignCenter)

        self.verticalLayout.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_wifi.setText(_translate("MainWindow", "WIFI"))
        self.label_login.setText(_translate("MainWindow", "Login"))
        self.label_password.setText(_translate("MainWindow", "Password"))
        self.label_ip_address.setText(_translate("MainWindow", "IP address"))
        self.label_ip.setText(_translate("MainWindow", "192.168.1.1"))


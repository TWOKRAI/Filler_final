# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Window_settings1/Window_pop_up/pop_up.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow_pop(object):
    def setupUi(self, MainWindow_pop):
        MainWindow_pop.setObjectName("MainWindow_pop")
        MainWindow_pop.resize(346, 236)
        self.centralwidget = QtWidgets.QWidget(MainWindow_pop)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 35, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 12, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_ok = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        spacerItem3 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 14, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        MainWindow_pop.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow_pop)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 346, 26))
        self.menubar.setObjectName("menubar")
        MainWindow_pop.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow_pop)
        self.statusbar.setObjectName("statusbar")
        MainWindow_pop.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_pop)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_pop)

    def retranslateUi(self, MainWindow_pop):
        _translate = QtCore.QCoreApplication.translate
        MainWindow_pop.setWindowTitle(_translate("MainWindow_pop", "MainWindow"))
        self.label_2.setText(_translate("MainWindow_pop", "Вы хотите сделать сброс параметров?"))
        self.pushButton_ok.setText(_translate("MainWindow_pop", "ПОДТВЕРДИТЬ"))
        self.pushButton_cancel.setText(_translate("MainWindow_pop", "ОТМЕНИТЬ"))

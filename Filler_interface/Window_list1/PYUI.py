# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Window_list1/UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(528, 407)
        MainWindow.setMinimumSize(QtCore.QSize(480, 320))
        MainWindow.setMaximumSize(QtCore.QSize(4800, 3200))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(456, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(27, 5, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.button_menu = QtWidgets.QPushButton(self.centralwidget)
        self.button_menu.setMinimumSize(QtCore.QSize(120, 90))
        font = QtGui.QFont()
        font.setFamily("Siemens AD Sans")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.button_menu.setFont(font)
        self.button_menu.setText("")
        self.button_menu.setObjectName("button_menu")
        self.verticalLayout_2.addWidget(self.button_menu)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setMinimumSize(QtCore.QSize(160, 90))
        font = QtGui.QFont()
        font.setFamily("Siemens AD Sans")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.button_start.setFont(font)
        self.button_start.setObjectName("button_start")
        self.verticalLayout.addWidget(self.button_start)
        spacerItem4 = QtWidgets.QSpacerItem(157, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem4)
        self.button_game = QtWidgets.QPushButton(self.centralwidget)
        self.button_game.setMinimumSize(QtCore.QSize(160, 90))
        font = QtGui.QFont()
        font.setFamily("Siemens AD Sans")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.button_game.setFont(font)
        self.button_game.setObjectName("button_game")
        self.verticalLayout.addWidget(self.button_game)
        spacerItem5 = QtWidgets.QSpacerItem(157, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)
        self.button_statistics = QtWidgets.QPushButton(self.centralwidget)
        self.button_statistics.setMinimumSize(QtCore.QSize(160, 90))
        font = QtGui.QFont()
        font.setFamily("Siemens AD Sans")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.button_statistics.setFont(font)
        self.button_statistics.setObjectName("button_statistics")
        self.verticalLayout.addWidget(self.button_statistics)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        spacerItem7 = QtWidgets.QSpacerItem(125, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        spacerItem8 = QtWidgets.QSpacerItem(27, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem9 = QtWidgets.QSpacerItem(456, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem9)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 528, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_start.setText(_translate("MainWindow", "Начать"))
        self.button_game.setText(_translate("MainWindow", "Игры"))
        self.button_statistics.setText(_translate("MainWindow", "Статистика"))

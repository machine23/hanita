# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_client_ui01.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 526)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: #F4F5F6;\n"
"}\n"
"QScrollBar:vertical {\n"
"     border: none;\n"
"     background: #F4F5F6;\n"
"     width: 8px;\n"
"     margin: 0;\n"
" }\n"
" QScrollBar::handle:vertical {\n"
"    border: 1px solid #F3F4F5;\n"
"    border-radius: 4px;\n"
"     background: lightgrey;\n"
"     min-height: 20px;\n"
" }\n"
"QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"     background: #F4F5F6;\n"
"     height: 20px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
" QScrollBar::sub-line:vertical {\n"
"     border: none;\n"
"     background: #F4F5F6;\n"
"     height: 20px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" \n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.splitter_2)
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.horizontalLayoutWidget_2)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.lw_list_chats = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lw_list_chats.sizePolicy().hasHeightForWidth())
        self.lw_list_chats.setSizePolicy(sizePolicy)
        self.lw_list_chats.setMinimumSize(QtCore.QSize(200, 300))
        self.lw_list_chats.setMaximumSize(QtCore.QSize(300, 16777215))
        self.lw_list_chats.setObjectName("lw_list_chats")
        self.verticalLayout_2.addWidget(self.lw_list_chats)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ql_current_chat = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ql_current_chat.setTextFormat(QtCore.Qt.PlainText)
        self.ql_current_chat.setAlignment(QtCore.Qt.AlignCenter)
        self.ql_current_chat.setObjectName("ql_current_chat")
        self.verticalLayout.addWidget(self.ql_current_chat)
        self.te_list_msg = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.te_list_msg.sizePolicy().hasHeightForWidth())
        self.te_list_msg.setSizePolicy(sizePolicy)
        self.te_list_msg.setMinimumSize(QtCore.QSize(0, 300))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 245, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.te_list_msg.setPalette(palette)
        self.te_list_msg.setAutoFillBackground(True)
        self.te_list_msg.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.te_list_msg.setFrameShadow(QtWidgets.QFrame.Plain)
        self.te_list_msg.setLineWidth(1)
        self.te_list_msg.setMidLineWidth(0)
        self.te_list_msg.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.te_list_msg.setUndoRedoEnabled(False)
        self.te_list_msg.setReadOnly(True)
        self.te_list_msg.setObjectName("te_list_msg")
        self.verticalLayout.addWidget(self.te_list_msg)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.te_input_msg = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.te_input_msg.setMaximumSize(QtCore.QSize(16777215, 200))
        self.te_input_msg.setObjectName("te_input_msg")
        self.horizontalLayout.addWidget(self.te_input_msg)
        self.pb_send = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_send.sizePolicy().hasHeightForWidth())
        self.pb_send.setSizePolicy(sizePolicy)
        self.pb_send.setMaximumSize(QtCore.QSize(16777215, 200))
        self.pb_send.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pb_send.setObjectName("pb_send")
        self.horizontalLayout.addWidget(self.pb_send)
        self.horizontalLayout_3.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hanita"))
        self.label.setText(_translate("MainWindow", "Chats:"))
        self.pushButton.setText(_translate("MainWindow", "New Chat"))
        self.pushButton_2.setText(_translate("MainWindow", "Contacts"))
        self.ql_current_chat.setText(_translate("MainWindow", "all"))
        self.pb_send.setText(_translate("MainWindow", "Send"))


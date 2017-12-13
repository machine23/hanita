# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_forms/main_client_ui01.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 526)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(
            """QMainWindow {
                    background-color: white;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #F4F5F6;
                    width: 8px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    border: 1px solid #F3F4F5;
                    border-radius: 4px;
                    background: lightgrey;
                    min-height: 20px;
                }
                QScrollBar::add-line:vertical {
                    border: none;
                    background: #F4F5F6;
                    height: 20px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }

                QScrollBar::sub-line:vertical {
                    border: none;
                    background: #F4F5F6;
                    height: 20px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: none;
                }
                QTextEdit {
                    background-color: white;
                }
                table {
                    background-color: blue;
                }
            """)
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
        self.pb_main_newchat = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_main_newchat.sizePolicy().hasHeightForWidth())
        self.pb_main_newchat.setSizePolicy(sizePolicy)
        self.pb_main_newchat.setObjectName("pb_main_newchat")
        self.verticalLayout_2.addWidget(self.pb_main_newchat)
        self.pb_main_contacts = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pb_main_contacts.setObjectName("pb_main_contacts")
        self.verticalLayout_2.addWidget(self.pb_main_contacts)
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.l_current_chat = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.l_current_chat.setTextFormat(QtCore.Qt.PlainText)
        self.l_current_chat.setAlignment(QtCore.Qt.AlignCenter)
        self.l_current_chat.setObjectName("l_current_chat")
        self.verticalLayout.addWidget(self.l_current_chat)
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
        self.pb_main_newchat.setText(_translate("MainWindow", "New Chat"))
        self.pb_main_contacts.setText(_translate("MainWindow", "Contacts"))
        self.l_current_chat.setText(_translate("MainWindow", "all"))
        self.pb_send.setText(_translate("MainWindow", "Send"))


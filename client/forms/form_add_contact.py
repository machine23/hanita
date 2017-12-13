# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './add_contact.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog_add_contact(object):
    def setupUi(self, dialog_add_contact):
        dialog_add_contact.setObjectName("dialog_add_contact")
        dialog_add_contact.resize(339, 563)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(dialog_add_contact)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.le_find_user = QtWidgets.QLineEdit(dialog_add_contact)
        self.le_find_user.setObjectName("le_find_user")
        self.verticalLayout.addWidget(self.le_find_user)
        self.lw_users = QtWidgets.QListWidget(dialog_add_contact)
        self.lw_users.setObjectName("lw_users")
        self.verticalLayout.addWidget(self.lw_users)
        self.pb_add_contact = QtWidgets.QPushButton(dialog_add_contact)
        self.pb_add_contact.setObjectName("pb_add_contact")
        self.verticalLayout.addWidget(self.pb_add_contact)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(dialog_add_contact)
        QtCore.QMetaObject.connectSlotsByName(dialog_add_contact)

    def retranslateUi(self, dialog_add_contact):
        _translate = QtCore.QCoreApplication.translate
        dialog_add_contact.setWindowTitle(_translate("dialog_add_contact", "Add Contact"))
        self.le_find_user.setPlaceholderText(_translate("dialog_add_contact", "Find..."))
        self.pb_add_contact.setText(_translate("dialog_add_contact", "Add Contact"))


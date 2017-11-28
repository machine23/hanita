import sys
import abc
from PyQt5 import QtWidgets
from sip import wrappertype
from .client_ui import Ui_MainWindow
# from .client import Client
from .client_db import ClientDB


class ClientMeta(wrappertype, abc.ABCMeta):
    pass


class BaseClientObserver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def model_is_changed(self):
        pass


class QtClientView(
        QtWidgets.QMainWindow, BaseClientObserver, metaclass=ClientMeta):
    app = QtWidgets.QApplication([])

    def __init__(self, client, client_model: ClientDB, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.controller = client
        self.model = client_model

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model.add_observer(self)

        self.ui.pb_send.clicked.connect(self.send)
        self.ui.lw_list_chats.itemDoubleClicked.connect(self.change_chat)

    def send(self):
        data = self.ui.te_input_msg.toPlainText()
        if data.strip():
            self.controller.send_msg_to(self.model.active_chat, data)
            self.ui.te_input_msg.setText("")

    def model_is_changed(self):
        self.render_messages()
        self.render_chats_list()
        pass

    def run(self):
        self.show()
        self.app.exec_()
        self.controller.close()

    def change_chat(self, item):
        chat_name = item.text()
        self.model.active_chat = chat_name
        self.ui.ql_current_chat.setText(chat_name)

    def render_info(self, info):
        msg = QtWidgets.QMessageBox()
        msg.setText(str(info))
        msg.exec()

    def input(self, msg):
        text, ok = QtWidgets.QInputDialog.getText(self, "Login",
                                                  "Enter your name")
        return text

    def render_message(self, message):
        pass

    def render_messages(self):
        """ 
        Отобразить все сообщения для чата
        """
        chat_name = self.model.active_chat
        messages = self.model.get_messages(chat_name)
        template = '''<div style="margin-bottom:50px;">
        <h4 style="color:blue;margin:0px;padding:0px;">{}: </h4>
        <p style="margin:0px;padding:0px;margin-left:10px;margin-bottom:20px;">{}</p>
        </div>'''

        arr = [
            template.format(i.from_user, i.message.replace("\n", "<br>"))
            for i in messages
        ]
        msg_string = "".join(arr)
        self.ui.te_list_msg.setHtml(msg_string)

    def render_chats_list(self):
        """
        get names of chats from db
        insert every name to list widget
        """
        chats = self.model.get_chats()
        self.ui.lw_list_chats.clear()
        self.ui.lw_list_chats.addItems(chats)

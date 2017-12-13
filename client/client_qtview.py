import abc
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from sip import wrappertype

# from .client_db import ClientDB
from .forms.app_ui import MainWindow
# from .client import Client
# from .forms.main_ui import Ui_MainWindow


# class ClientMeta(wrappertype, abc.ABCMeta):
#     pass


# class BaseClientObserver(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def model_is_changed(self):
#         pass


class QtClientView(MainWindow):
    """ Класс представления пользовательского интерфейса """
    app = QtWidgets.QApplication([])
    model_changed = pyqtSignal()

    def __init__(self, client=None, parent=None):
        super().__init__(parent)
        self.controller = client
        self.client_db = None
        self.thread = None

    def set_client_db(self, client_db):
        """ Передать объект хранилища, откуда будет браться инфо
        для отображения
        """
        self.client_db = client_db
        if self.client_db:
            self.client_db.add_observer(self)


    def run(self):
        """ Запускает цикл интерфейса """
        ################
        self.thread = QThread()
        self.controller.moveToThread(self.thread)
        self.thread.started.connect(self.render)
        self.thread.started.connect(self.controller.receive)
        self.thread.start()
        ################
        self.show()
        self.app.exec_()

    def render_info(self, info):
        """ Отрисовывает информационное окно. """
        msg = QtWidgets.QMessageBox()
        msg.setText(str(info))
        msg.exec()

    def input(self, msg):
        """ Отрисовывает окно с вопросом и полем ввода для ответа. """
        text, ok = QtWidgets.QInputDialog.getText(self, "Login",
                                                  "Enter your name")
        return text

    def get_chatlist(self):
        """ Получить список чатов. """
        chat_ids = self.client_db.get_chats()
        chats = []
        for _id in chat_ids:
            chat = self.client_db.get_chat(_id)
            chats.append(chat)
        return chats
    
    def get_contactlist(self):
        """ Получить список контактов. """
        contacts = self.client_db.get_contacts(self.current_user["user_id"])
        return contacts

    def get_msgslist(self):
        msgs_ids = self.client_db.get_msgs(self.current_chat["chat_id"])
        print("get_msgslist", msgs_ids)
        msgs = []
        for _id in msgs_ids:
            msg = self.client_db.get_msg(_id)
            user_id = msg["user_id"]
            user_name = self.client_db.get_user(user_id)["user_name"]
            timestamp = msg["timestamp"]
            message = msg["message"]
            msg_out = {"user_id": user_id, "user_name":user_name, "timestamp":timestamp, "message":message}
            msgs.append(msg_out)
        return msgs

    def get_handle_msg(self, data):
        print("qtview get_handle_msg:", data)
        self.controller.send_to_server(data)





if __name__ == "__main__":
    app = QtClientView()
    app.run()

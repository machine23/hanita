import sys
import abc
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
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
    model_changed = pyqtSignal()

    def __init__(self, client, client_model=None, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.controller = client
        self.set_model(client_model)

        self.thread = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pb_send.clicked.connect(self.send)
        self.ui.lw_list_chats.itemDoubleClicked.connect(self.change_chat)

    def set_model(self, client_model: ClientDB):
        """ Получить БД """
        self.model = client_model
        if self.model:
            self.model.add_observer(self)

    def send(self):
        data = self.ui.te_input_msg.toPlainText()
        if data.strip():
            self.controller.send_msg_to(self.model.active_chat, data)
            self.ui.te_input_msg.setText("")
            self.ui.te_input_msg.setFocus()

    def model_is_changed(self):
        print("model_is_changed")
        self.model_changed.emit()

    def render_view(self):
        print("render_view")
        self.render_messages()
        self.render_chats_list()
    #     pass

    def run(self):
        ################
        self.model_changed.connect(self.render_view)
        self.thread = QThread()
        self.controller.moveToThread(self.thread)
        self.thread.started.connect(self.render_view)
        self.thread.started.connect(self.controller.receive)
        self.thread.start()
        print(self.thread.isRunning())
        ################
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
        user = self.model.active_user
        messages = self.model.get_messages(chat_name)
        template = '''
        <table 
            bgcolor="#fff" 
            width="100%" 
            style="margin:5px {left} 5px {right};">
            <tr>
                <td style="padding:5px 15px;">
                    <b style="color:{color};">
                        {name}
                    </b>
                </td>
            </tr>
            <tr>
                <td style="padding:0px 20px 10px;">
                    {text}
                </td>
            </tr>
        </table>
        '''

        arr = [
            template.format(
                left="5px" if i.from_user == user else "25px",
                right="25px" if i.from_user == user else "5px",
                color="orange" if i.from_user == user else "blue",
                name=i.from_user,
                text=i.message.replace("\n", "<br>"))
            for i in messages
        ]
        msg_string = '<body bgcolor="#F4F5F6">'+"".join(arr)+'<a name="end" style="color:#F4F5F6">a</a>'+'</html>'
        self.ui.te_list_msg.setHtml(msg_string)
        self.ui.te_list_msg.scrollToAnchor("end")

    def render_chats_list(self):
        """
        get names of chats from db
        insert every name to list widget
        """
        chats = self.model.get_chats()
        self.ui.lw_list_chats.clear()
        self.ui.lw_list_chats.addItems(chats)

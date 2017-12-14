""" Hanita client class and client mainloop """
import random
import sys
import threading
import time

from PyQt5.QtCore import QObject

from JIM import JIMClientMessage, JIMMessage, JIMResponse

from .client_connection import ClientConnection, ClientConnectionError
from .client_db import ClientDB, ClientDBError
from .client_qtview import QtClientView

WAITING_TIME = 1.0


###############################################################################
# ### ClientError
###############################################################################
class ClientError(Exception):
    """ Класс для ошибок клиента """
    pass


###############################################################################
# ### class ClientUser
###############################################################################
class ClientUser:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name


###############################################################################
# class Client
###############################################################################
class Client:
    """ класс Client """

    def __init__(self, conn: ClientConnection, ViewClass):
        super().__init__()
        # self.user = ClientUser()
        self.self_id = None
        self.client_db = None
        self.conn = conn
        self.view = ViewClass(self)
        self.msg_handlers = {
            JIMMessage.MSG: self.handle_msg,
            JIMMessage.CONTACT_LIST: self.handle_contact,
            JIMMessage.CHAT_INFO: self.handle_chat_info,

        }
        try:
            self.conn.connect()
        except ClientConnectionError:
            self.view.render_info("Не могу соединиться с сервером")
            self.conn = None
            self.close()

    def send_presence(self):
        """ Сообщаем серверу о присутствии """
        msg = JIMClientMessage.presence()
        self.send_to_server(msg)

    def authenticate(self):
        """ Аутентификация пользователя """
        # Пока все просто, без пароля
        login = self.view.input("Login: ").strip()
        if not login:
            self.view.render_info(
                "Имя не может быть пустым или состоять из пробелов")
            sys.exit()
        msg = JIMClientMessage.authenticate(login, "")
        resp = self.send_and_get(msg)
        print("clint autehenticate resp:", resp)
        if resp.response:
            if resp.error:
                self.view.render_info(resp.error)
                return False
            else:
                db_name = login + ".db"
                self.client_db = ClientDB(db_name)
                self.view.set_client_db(self.client_db)
                ###
                self.view.current_user = resp["user"]
                self.client_db.active_user = resp["user"]

                ###
                return True

    def send_to_server(self, message):
        """
        Отправляем на сервер сообщение от пользователя.
        """
        # msg = JIMClientMessage.msg(chat_id, message)
        # self.client_db.add_msg(**msg)
        self.conn.send(message)

    def send_and_get(self, message):
        """
        Отправляем на сервер и обрабатываем ответ от сервера.
        """
        self.conn.send(message)
        resp = None
        start = time.time()
        while resp is None:
            resp = self.conn.get()
            if time.time() - start > WAITING_TIME:
                self.view.render_info("Потеряна связь с сервером")
                break
        return resp

    def get_from(self):
        """ Получаем и обрабатываем сообщение, присланное от другого клиента """
        msg = self.conn.get()
        if msg and msg.action:
            print("client get_from msg:", msg)
            self.msg_handlers[msg.action](msg)

    def handle_msg(self, msg):
        """ Обработка сообщения msg """
        print("handle_msg msg", msg)
        msg_id = msg.msg_id
        user = msg.user
        chat_id = msg.chat_id
        if not self.client_db.msg_exists(msg_id):
            self.client_db.add_msg(
                msg_id, user["user_id"], chat_id, msg.timestamp, msg.message)

    def handle_contact(self, msg):
        """ Обработка сообщения contact_list """
        print("handle_contact msg:", msg)
        contacts = msg["contacts"]
        for contact in contacts:
            user_id = contact["user_id"]
            user_name = contact["user_name"]
            self.client_db.update_user(user_id, user_name, True)

    def handle_chat_info(self, msg):
        """ Обработка сообщения chat_list """
        print("handle_chat_info msg:", msg)
        chat_id = msg.chat["chat_id"]
        chat_name = msg.chat["chat_name"]
        chat_users = msg.chat_users
        if not chat_name:
            chat_name = self.create_chat_name(chat_users)
        if not self.client_db.chat_exists(chat_id):
            self.client_db.add_chat(chat_id, chat_name)
        for user in chat_users:
            self.client_db.update_user(user["user_id"], user["user_name"])

    def create_chat_name(self, users):
        """ Создает имя чата на основе списка пользователей чата. """
        users_len = len(users)
        if not users_len:
            return
        elif users_len == 1:
            return users[0]["user_name"]
        user_names = [
            user["user_name"] for user in users
            if user["user_name"] != self.client_db.active_user["user_name"]
        ]
        chat_name = ", ".join(user_names)
        return chat_name


    def run(self):
        """ Главный цикл работы клиента """
        while not self.authenticate():
            pass
        msg = JIMClientMessage.get_chats()
        self.send_to_server(msg)
        self.view.run()
        # self.view.render_info("Good bye!")
        self.close()

    def receive(self):
        """ Получаем сообщения от сервера """
        while True:
            self.get_from()

    def parse_msg(self, msg):
        """ Разбор сообщений пришедших с сервера """
        action = msg.action
        if msg.action:
            pass

    def close(self, info=""):
        """ Закрываем клиент """
        msg = JIMClientMessage.quit()
        print("close client")
        if self.conn:
            self.conn.send(msg)
            self.conn.close()
            self.conn = None
        if self.client_db:
            self.client_db.close()
            self.client_db = None
        if info:
            self.view.render_info(info)
        sys.exit()


class QtClient(Client, QObject):
    pass

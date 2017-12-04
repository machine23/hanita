""" Hanita client class and client mainloop """
import sys
import time
import threading
import random

from PyQt5.QtCore import QObject

from JIM import JIMClientMessage, JIMResponse, JIMMessage

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
    def __init__(self, name="", status=""):
        self.name = name
        self.status = status
        self.contacts = []


###############################################################################
# class Client
###############################################################################
class Client:
    """ класс Client """

    def __init__(self, conn: ClientConnection, ViewClass):
        super().__init__()
        self.user = ClientUser()
        # db_name = "client" + str(random.randint(1, 100000)) + ".db"
        self.model = None
        self.conn = conn
        self.view = ViewClass(self)
        try:
            self.conn.connect()
        except ClientConnectionError:
            self.view.render_info("Не могу соединиться с сервером")
            self.conn = None
            self.close()

    def send_presence(self):
        """ Сообщаем серверу о присутствии """
        msg = JIMClientMessage.presence(self.user.name)
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
        resp = self.send_to_server(msg)
        if resp.response and resp.error:
            self.view.render_info(resp.error)
            return False
        self.user.name = login
        db_name = login + ".db"
        self.model = ClientDB(db_name)
        self.view.set_model(self.model)
        # self.view.render_info("Привет, " + login + "!")
        ###
        self.model.active_user = login
        self.model.active_chat = "#all"
        ###
        return True

    def send_msg_to(self, to_user, message):
        """
        Отправляем на сервер сообщение от пользователя.
        """
        msg = JIMClientMessage.msg(self.user.name, to_user, message)
        ###
        self.model.add_message(msg)
        ###
        resp = self.conn.send(msg)
        # if resp.error:
        #     self.view.render_info(resp.error)
        #     pass

    def send_to_server(self, message):
        """
        Отправляем на сервер и обрабатываем ответ от сервера.
        """
        # self.conn.get()  # отбрасываем нежданное сообщение перед отправкой
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
        # if msg is None:
        #     self.close("Потеряна связь с сервером")
        if msg and msg.action == msg.MSG:
            print("get_from:", msg)
            self.view.render_message(msg)
            ###
            self.model.add_message(msg)
            ###

    def run(self, mode=None):
        """ Главный цикл работы клиента """
        while not self.authenticate():
            pass
        # if mode == "read":
        #     # self.view.render_help()
        #     while True:
        #         self.get_from()
        # elif mode == "write":
        print("*** run ***")
        self.view.run()
        self.view.render_info("Good bye!")
        self.close()

    def receive(self):
        print("receive")
        while True:
            self.get_from()

    def parse_cmd(self, user_msg: str):
        """ Разбираем команды пользователя """
        user_msg = user_msg.strip()
        if user_msg.startswith("!") or user_msg.startswith("@"):
            if len(user_msg.split(" ")) > 1:
                cmd, msg = user_msg.split(" ", 1)
            else:
                cmd, msg = user_msg, ""
            #
            if cmd == "!quit":
                self.close("Good bye")
            elif cmd == "!contacts":
                self.get_contacts()
            elif cmd == "!add":
                self.add_contact(msg)
            elif cmd == "!del":
                self.del_contact(msg)
            elif cmd == "!help":
                self.view.render_help()
                pass
            elif cmd == "@":
                self.who_online()
            elif cmd.startswith("@") and len(cmd) > 1:
                self.send_msg_to(cmd[1:], msg)
            else:
                self.view.render_info("Неизвестная команда!")
                pass
            return True
        return False

    def get_contacts(self):
        """ Получить контакты """
        msg = JIMClientMessage.get_contacts()
        resp = self.send_to_server(msg)
        if resp.response == 202:
            if resp.quantity:
                while len(self.user.contacts) < resp.quantity:
                    contact = self.conn.get()
                    if contact.action == JIMMessage.CONTACT_LIST:
                        self.user.contacts.append(contact.user_id)
                        ###
                        self.model.add_user(contact.user_id)
                        ###
                self.view.render_contacts(self.user.contacts, "Ваши контакты:")
            else:
                self.view.render_info("У вас нет контактов")
        else:
            self.view.render_info("get_contacts" + str(resp))

    def add_contact(self, nickname):
        """ Добавить контакт """
        msg = JIMClientMessage.add_contact(nickname)
        resp = self.send_to_server(msg)
        if resp.error:
            self.view.render_info("Не удалось добавить контакт")
            # self.view.render_info(resp.error)
            pass
        else:
            self.user.contacts.append(nickname)
            ###
            self.model.add_user(nickname)
            ###

    def del_contact(self, nickname):
        """ Удалить контакт """
        msg = JIMClientMessage.del_contact(nickname)
        resp = self.send_to_server(msg)
        if resp.error:
            self.view.render_info("Не удалось удалить контакт")
            # self.view.render_info(resp.error)
            pass
        else:
            if nickname in self.user.contacts:
                self.user.contacts.remove(nickname)

    def who_online(self):
        """ Узнать, кто онлайн """
        online_users = []
        msg = JIMClientMessage.who_online()
        resp = self.send_to_server(msg)
        if resp.response == 202 and resp.quantity:
            while len(online_users) < resp.quantity:
                contact = self.conn.get()
                if contact.action == JIMMessage.ONLINE_LIST:
                    online_users.append(contact.user_id)
            self.view.render_contacts(online_users, "Онлайн:")
        else:
            self.view.render_info(resp)
            pass

    def close(self, info=""):
        """ Закрываем клиент """
        msg = JIMClientMessage.quit()
        print("close client")
        if self.conn:
            self.conn.send(msg)
            self.conn.close()
            self.conn = None
        if info:
            self.view.render_info(info)
        sys.exit()


class QtClient(Client, QObject):
    pass
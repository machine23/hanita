""" Hanita client class and client mainloop """
import argparse
import sys

from JIM import JIMClientMessage, JIMResponse, JIMMessage

from .client_connection import ClientConnection, ClientConnectionError
from .client_view import BaseClientView, ConsoleClientView


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

    def __init__(self, conn: ClientConnection, view: BaseClientView):
        self.user = ClientUser()
        self.conn = conn
        self.view = view
        try:
            self.conn.connect()
        except ClientConnectionError as err:
            self.view.render_info(err)
            self.conn = None            
            self.close()

    def send_presence(self):
        """ Сообщаем серверу о присутствии """
        msg = JIMClientMessage.presence(self.user.name)
        self.send_to_server(msg)

    def authenticate(self):
        """ Аутентификация пользователя """
        # Пока все просто, без пароля
        while True:
            login = self.view.input("Login: ").strip()
            if login:
                break
            self.view.render_info(
                "Имя не может быть пустым или состоять из пробелов")
        msg = JIMClientMessage.authenticate(login, "")
        resp = self.send_to_server(msg)
        if resp.response and resp.error:
            self.view.render_info(resp.error)
            return False
        self.user.name = login
        self.view.render_info("Привет, " + login + "!")
        return True

    def send_msg_to(self, to_user, message):
        """
        Отправляем на сервер сообщение от пользователя.
        """
        msg = JIMClientMessage.msg(self.user.name, to_user, message)
        resp = self.send_to_server(msg)
        if resp.error:
            self.view.render_info(resp.error)

    def send_to_server(self, message):
        """
        Отправляем на сервер и обрабатываем ответ от сервера.
        """
        self.conn.get()  # отбрасываем нежданное сообщение перед отправкой
        self.conn.send(message)
        resp = self.conn.get()
        # print("response:", resp)
        if resp is None:
            self.close("Потеряна связь с сервером")
        else:
            return resp

    def get_from(self):
        """ Получаем и обрабатываем сообщение, присланное от другого клиента """
        msg = self.conn.get()
        # if msg is None:
        #     self.close("Потеряна связь с сервером")
        if msg and msg.action == msg.MSG:
            self.view.render_message(msg)

    def run(self, mode=None):
        """ Главный цикл работы клиента """
        while not self.authenticate():
            pass
        self.view.render_help()
        while True:
            if mode == "read":
                self.get_from()
            elif mode == "write":
                user_msg = self.view.input(">>> ")
                if not self.parse_cmd(user_msg):
                    self.send_msg_to("#all", user_msg)
            else:
                break
        self.view.render_info("Good bye!")
        self.close()

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
            elif cmd == "@":
                self.who_online()
            elif cmd.startswith("@") and len(cmd) > 1:
                self.send_msg_to(cmd[1:], msg)
            else:
                self.view.render_info("Неизвестная команда!")
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
            self.view.render_info(resp.error)
        else:
            self.user.contacts.append(nickname)

    def del_contact(self, nickname):
        """ Удалить контакт """
        msg = JIMClientMessage.del_contact(nickname)
        resp = self.send_to_server(msg)
        if resp.error:
            self.view.render_info("Не удалось удалить контакт")
            self.view.render_info(resp.error)
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

    def close(self, info=""):
        """ Закрываем клиент """
        msg = JIMClientMessage.quit()
        if self.conn:
            self.send_to_server(msg)
            self.conn.close()
        if info:
            self.view.render_info(info)
        sys.exit()


###############################################################################
# read_args
###############################################################################
def read_args():
    """
    Получаем аргументы командной строки.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "addr",
        default="127.0.0.1",
        nargs="?",
        help="IP сервера (по умолчанию 127.0.0.1)"
    )
    parser.add_argument(
        "port",
        type=int,
        default=7777,
        nargs="?",
        help="TCP-порт сервера (по умолчанию 7777)"
    )
    parser.add_argument(
        "-r",
        dest="read",
        action="store_true",
        help="определяет режим работы на получение сообщений"
    )
    parser.add_argument(
        "-w",
        dest="write",
        action="store_true",
        help="включает режим отправки сообщений"
    )

    args = parser.parse_args()
    if args.read and args.write:
        print(
            "Пожалуйста, определите режим работы:",
            "\n\t-w на отправку сообщений",
            "\n\t-r на получение сообщений"
        )
        sys.exit(0)
    return args


###############################################################################
# main
###############################################################################
def main():
    """ Точка входа """
    args = read_args()
    if args.write:
        mode = "write"
    elif args.read:
        mode = "read"
    else:
        mode = None

    connection = ClientConnection(args.addr, args.port)
    view = ConsoleClientView()

    client = Client(connection, view)
    try:
        client.run(mode)
    except KeyboardInterrupt:
        pass

    client.close("Good Bye!")



###############################################################################
if __name__ == "__main__":
    main()

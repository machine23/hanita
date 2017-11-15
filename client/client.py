""" Hanita client class and client mainloop """
import argparse
import sys

from JIM import JIMClientMessage

from .client_connection import ClientConnection, ClientConnectionError
from .client_view import BaseClientView, ConsoleClientView


###############################################################################
# ### ClientError
###############################################################################
class ClientError(Exception):
    """ Класс для ошибок клиента """
    pass


###############################################################################
# class Client
###############################################################################
class Client:
    """ класс Client """

    def __init__(self, user: str, conn: ClientConnection, view: BaseClientView):
        self.user = user
        self.conn = conn
        self.view = view
        try:
            self.conn.connect()
        except ClientConnectionError as err:
            self.close(err)

    def send_presence(self):
        """ Сообщаем серверу о присутствии """
        msg = JIMClientMessage.presence(self.user)
        self.send_to_server(msg)

    def send_msg(self, to_user, message):
        """
        Отправляем на сервер сообщение от пользователя.
        """
        msg = JIMClientMessage.msg(self.user, to_user, message)
        self.send_to_server(msg)

    def send_to_server(self, message):
        """
        Отправляем на сервер и обрабатываем ответ от сервера.
        """
        self.conn.send(message)
        resp = self.conn.get()
        if resp is None:
            self.close("Потеряна связь с сервером")
        if resp.error:
            self.view.render_info(resp.error)

    def get_from(self):
        """ Получаем и обрабатываем сообщение, присланное от другого клиента """
        msg = self.conn.get()
        if msg is None:
            self.close("Потеряна связь с сервером")
        if msg.action == msg.MSG:
            self.view.render_message(msg)

    def run(self, mode=None):
        """ Главный цикл работы клиента """
        self.send_presence()
        while True:
            if mode == "read":
                self.get_from()
            elif mode == "write":
                user_msg = input(">>> ")
                self.send_msg("#all", user_msg)
            else:
                break
        self.view.render_info("Good bye!")
        self.close()

    def close(self, info=""):
        """ Закрываем клиент """
        if self.conn:
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

    client = Client("Guest", connection, view)
    try:
        client.run(mode)
    except KeyboardInterrupt:
        pass

    client.close("Good Bye!")



###############################################################################
if __name__ == "__main__":
    main()

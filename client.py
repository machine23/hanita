""" Hanita client class and client mainloop """
import argparse
import json
import socket
import sys
import time

import actions

RECV_BUFFER = 1024


class ClientError(Exception):
    """ Класс для ошибок клиента """
    pass


###############################################################################
# class Client
###############################################################################
class Client:
    """ класс Client """

    def __init__(self, user, status=""):
        self.user = user
        self.status = status
        self.addr = None
        self.port = None
        self.connection = None

    def connect(self, addr="", port=7777):
        """ Устанавливаем соединение с сервером """
        if self.connection:
            raise ClientError("Соединение уже установлено")

        self.addr = addr
        self.port = port
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((addr, port))
        except socket.error:
            raise ClientError("Ошибка установки соединения")

    def create_message(self, action, to_user=None, message=None,
                       status=None, timestamp=None):
        """ Формируем сообщение """
        if action not in actions.actions_list:
            raise ClientError("Неправильный action")
        if timestamp is None:
            timestamp = time.time()

        msg = None
        if action == actions.PRESENCE:
            msg = actions.create_presence(self.user,
                                          status=status, timestamp=timestamp)
        elif action == actions.MSG:
            msg = actions.create_msg(
                self.user, to_user, message, timestamp=timestamp)
        return msg

    def send(self, message):
        """ Отсылаем сообщение на сервер """
        if self.connection is None:
            raise ClientError("Нет соединения")
        msg = json.dumps(message)
        self.connection.sendall(msg.encode("utf-8"))

    @staticmethod
    def parse_response(resp):
        """ Разбираем ответ от сервера """
        return json.loads(resp)

    def get(self):
        """ Получаем ответ от сервера """
        if self.connection is None:
            raise ClientError("Нет соединения")
        resp = self.connection.recv(RECV_BUFFER)
        if not resp:
            raise ClientError("Пропало соединение с сервером")
        return self.parse_response(resp)

    def close(self):
        """ Закрываем клиент """
        if self.connection:
            self.connection.close()
            self.connection = None


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
# send_presence
###############################################################################
def send_presence(user):
    """
    Отправка сообщения Presence на сервер.
    """
    msg = user.create_message(actions.PRESENCE)

    user.send(msg)
    resp = user.get()

    if resp:
        print("Response from server:", end="")
        print(resp["response"], resp["alert"])


###############################################################################
# input_and_send
###############################################################################
def input_and_send(user):
    """
    Ввод и отправка сообщения.
    Ввод пустой строки завершает приложение
    """
    user_msg = input("Ваше сообщение: ")
    if not user_msg:
        print("Good bye")
        user.close()
        sys.exit(0)
    msg = user.create_message(actions.MSG, "#chat", user_msg)
    user.send(msg)
    try:
        resp = user.get()
    except ClientError as err:
        print(err)
        user.close()
        sys.exit(0)
    if resp:
        if "alert" in resp:
            print(resp["alert"])
        elif "error" in resp:
            print(resp["error"])
        else:
            print(resp)


###############################################################################
# get_and_print
###############################################################################
def get_and_print(user):
    """
    Получаем сообщение от сервера и вывод его в консоль.
    """
    try:
        msg = user.get()
    except ClientError as err:
        print(err)
        user.close()
        sys.exit(0)
    if msg and msg["action"] == actions.MSG:
        name = msg["from"]
        message = msg["message"]
        print("{}: {}".format(name, message))


###############################################################################
# main
###############################################################################
def main():
    """ Точка входа """
    args = read_args()

    user = Client("John Doe")
    try:
        user.connect(args.addr, args.port)
    except ClientError:
        print("Не удается подключится к серверу")
        user.close()
        sys.exit(0)

    send_presence(user)

    if args.write:
        while True:
            input_and_send(user)
    elif args.read:
        while True:
            get_and_print(user)

    user.close()



###############################################################################
if __name__ == "__main__":
    main()

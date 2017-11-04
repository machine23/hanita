import argparse
import json
import socket
import sys
import time
from pprint import pprint

import actions


RECV_BUFFER = 1024


class ClientError(Exception):
    """ Класс для ошибок клиента """
    pass


###############################################################################
# class Client
###############################################################################
class Client:
    def __init__(self, user, status=""):
        self.user = user
        self.status = status
        self.addr = None
        self.port = None
        self.connection = None

    def connect(self, addr="", port=7777):
        if self.connection:
            raise ClientError("Соединение уже установлено")

        self.addr = addr
        self.port = port
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((addr, port))
        except socket.error as err:
            raise ClientError("Ошибка установки соединения: " + str(err))

    def create_message(self, action, to_user=None, message=None, timestamp=None):
        """ Формируем сообщение """
        if action not in actions.actions_list:
            raise ClientError("Не правильный action")
        if timestamp is None:
            timestamp = time.time()

        msg = None
        if action == actions.PRESENCE:
            msg = actions.create_presence(self.user)
        elif action == actions.MSG:
            msg = actions.create_msg(self.user, to_user, message)
        return msg

    def send(self, message):
        """ Отсылаем сообщение на сервер """
        if self.connection is None:
            raise ClienError("Нет соединения")
        msg = json.dumps(message)
        self.connection.sendall(msg.encode("utf-8"))

    def get_response(self):
        """ Получаем ответ от сервера """
        if self.connection is None:
            raise ClientError("Нет соединения")
        resp = self.connection.recv(RECV_BUFFER)
        return resp

    def parse_response(self, resp):
        """ Разбираем ответ от сервера """
        return json.loads(resp)

    def close(self):
        """ Закрываем клиент """
        if self.connection:
            self.connection.close()
            self.connection = None


###############################################################################
# read_args
###############################################################################
def read_args():
    """ Получаем аргументы командной строки """
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
        action="store_true",
        help="определяет режим работы на получение сообщений"
    )
    parser.add_argument(
        "-w",
        action="store_true",
        help="включает режим отправки сообщений"
    )

    args = parser.parse_args()
    if args.r == args.w:
        print(
            "Пожалуйста, определите режим работы:",
            "\n\t-w на отправку сообщений",
            "\n\t-r на получение сообщений"
        )
        quit()
    return args


###############################################################################
# main
###############################################################################
def main():
    """ Точка входа """
    args = read_args()

    user = Client("John Doe")
    try:
        user.connect(args.addr, args.port)
        msg = user.create_message(actions.PRESENCE, time.time())

        user.send(msg)
        resp = user.get_response()

        if resp:
            print("Response from server:", end="")
            pprint(user.parse_response(resp))

    except Exception as err:
        raise ClientError("Что-то пошло не так") from err

    finally:
        user.close()


###############################################################################
if __name__ == "__main__":
    main()

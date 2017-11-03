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

    def create_msg(self, action, timestamp=None):
        """ Формируем сообщение """
        msg = {
            "action": action,
            "time": timestamp,
            "type": "status",
            "user": {
                "account_name": self.user,
                "status": self.status
            }
        }
        return msg

    def send(self, message):
        """ Отсылаем сообщение на сервер """
        if not self.connection:
            raise ClienError("Нет соединения")

        msg = json.dumps(message)
        self.connection.sendall(msg.encode("utf-8"))
        print("Send to {}:{} {}".format(self.addr, self.port, message))

    def get_response(self):
        """ Получаем ответ от сервера """
        if not self.connection:
            raise ClientError("Нет соединения")

        resp = self.connection.recv(RECV_BUFFER)
        return resp

    def parse_response(self, resp):
        """ Разбираем ответ от сервера """
        r = json.loads(resp)
        return r

    def close(self):
        """ Закрываем клиент """
        if self.connection:
            self.connection.close()
            self.connection = None


###################################################
def main():
    """ Точка входа """
    parser = argparse.ArgumentParser()
    parser.add_argument("addr", default="127.0.0.1", nargs="?",
                        help="IP сервера (по умолчанию 127.0.0.1)")
    parser.add_argument("port", type=int, default=7777, nargs="?",
                        help="TCP-порт сервера (по умолчанию 7777)")
    args = parser.parse_args()

    user = Client("John Doe")
    try:
        user.connect(args.addr, args.port)
        msg = user.create_msg(actions.PRESENCE, time.time())

        user.send(msg)
        resp = user.get_response()

        if resp:
            print("Response from server:", end="")
            pprint(user.parse_response(resp))

    except Exception as err:
        raise ClientError("Что-то пошло не так") from err

    finally:
        user.close()


#########################
if __name__ == "__main__":
    main()

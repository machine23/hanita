""" server.py """
import argparse
import json
import select
import socket

import actions

RECV_BUFFER = 1024


class ServerError(Exception):
    """ класс для ошибок сервера """
    pass


###############################################################################
# Server
###############################################################################
class Server:
    """ class Server """

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.clients = []
        self.requests = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((self.addr, self.port))
            self.sock.listen(5)
            self.sock.settimeout(0.2)
            print("\nStarting server at http://{}:{}"
                  .format(self.addr, self.port))
        except Exception:
            self.close()
            raise

    def accept(self):
        """ Разрешаем подключиться клиенту """
        try:
            client, client_addr = self.sock.accept()
        except OSError:
            pass
        else:
            print("Запрос на соединение от", client_addr)
            self.clients.append(client)

    def get(self, client):
        """ Получаем сообщение от клиента """
        if client not in self.clients:
            raise ServerError("get: Неизвестный клиент")
        try:
            bmsg = client.recv(RECV_BUFFER)
        except socket.error:
            client.close()
            self.clients.remove(client)
        else:
            if bmsg:
                msg = self.parse_msg(bmsg)
                self.send(client, self.create_response(msg))
                return msg

    def run_chat(self):
        """ Запускаем чат """
        wait = 0
        r = []
        w = []
        try:
            r, w, _ = select.select(self.clients, self.clients, [], wait)
        except InterruptedError:
            pass
        for client in r:
            try:
                msg = self.get(client)
            except ServerError:
                pass
            else:
                if msg and msg["action"] == actions.MSG:
                    self.send_from_to_all(client, w, msg)

    @staticmethod
    def parse_msg(message):
        """ Парсим сообщение от клиента """
        return json.loads(message.decode("utf-8"))

    @staticmethod
    def check_msg(message):
        """ Проверяем соответствие сообщения протоколу """
        if isinstance(message, dict):
            return message["action"] in actions.actions_list
        return False

    def create_response(self, message):
        """ Формируем ответ клиенту """
        if self.check_msg(message):
            return {"response": 200, "alert": "ok"}
        return {"response": 400, "error": "неправильный запрос/JSON-объект"}

    def send(self, client, message):
        """ Отправляем сообщение клиенту """
        if client not in self.clients:
            raise ServerError("send: Неизвестный клиент")
        if isinstance(message, dict):
            msg = json.dumps(message)
            try:
                client.sendall(msg.encode("utf-8"))
            except socket.error:
                client.close()
                self.clients.remove(client)
        else:
            raise ServerError("неправильный формат ответа")

    def send_from_to_all(self, _from, to_whom, message):
        """ Отправляем сообщение от клиента всем остальным """
        if isinstance(to_whom, list):
            for client in to_whom:
                if client is not _from:
                    self.send(client, message)

    def clients_close(self):
        """ Закрываем соединение с клиентом """
        for client in self.clients:
            client.close()
        self.clients.clear()

    def close(self):
        """ Закрываем сервер """
        self.clients_close()
        if self.sock:
            self.sock.close()
            self.sock = None


###############################################################################
# read_args
###############################################################################
def read_args():
    """ Читаем аргументы командной строки """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        dest="addr",
        default="127.0.0.1",
        help="IP-адрес для прослушивания"
    )
    parser.add_argument(
        "-p",
        dest="port",
        type=int,
        default=7777,
        help="TCP-порт (по умолчанию 7777)"
    )

    args = parser.parse_args()
    return args


###############################################################################
# main
###############################################################################
def main():
    """ mainloop """
    args = read_args()

    server = Server(args.addr, args.port)

    try:
        while True:
            server.accept()
            server.run_chat()

    except KeyboardInterrupt:
        print("\nServer close")

    server.close()


###############################################################################
#
###############################################################################
if __name__ == "__main__":
    main()

import argparse
import json
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
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.client = None
        self.client_addr = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((self.addr, self.port))
            self.sock.listen()
            print("\nStarting server at http://{}:{}"
                  .format(self.addr, self.port))
        except Exception:
            self.close()
            raise

    def accept(self):
        """ Разрешаем подключиться клиенту """
        if self.client is None:
            self.client, self.client_addr = self.sock.accept()
            print("Запрос на соединение от", self.client_addr)

    def get(self):
        """ Получаем сообщение от клиента """
        if self.client is None:
            raise ServerError("Нет присоединенных клиентов")
        msg = self.client.recv(RECV_BUFFER)
        return self.parse_msg(msg) if msg else None

    def parse_msg(self, message):
        """ Парсим сообщение от клиента """
        return json.loads(message.decode("utf-8"))

    def create_response(self, message):
        """ Формируем ответ клиенту """
        if isinstance(message, dict):
            if message["action"] in actions.actions_list:
                return {"response": 200, "alert": "ok"}
        return {"response": 400, "error": "неправильный запрос/JSON-объект"}

    def send(self, response):
        """ Отправляем сообщение клиенту """
        if self.client is None:
            raise ServerError("Нет присоединенных клиентов")
        if isinstance(response, dict):
            resp = json.dumps(response)
            self.client.sendall(resp.encode("utf-8"))
            print("Send to", self.client_addr, resp)
        else:
            raise ServerError("неправильный формат ответа")

    def client_close(self):
        """ Закрываем соединение с клиентом """
        if self.client:
            self.client.close()
            self.client = None
            self.client_addr = None

    def close(self):
        """ Закрываем сервер """
        self.client_close()
        if self.sock:
            self.sock.close()
            self.sock = None


###############################################################################
# read_args
###############################################################################
def read_args():
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
    args = read_args()

    server = Server(args.addr, args.port)

    try:
        while True:
            server.accept()
            msg = server.get()
            if msg:
                print("msg", msg)
                resp = server.create_response(msg)
                server.send(resp)
            else:
                server.client_close()

    except KeyboardInterrupt:
        print("Server close")

    server.close()


###############################################################################
#
###############################################################################
if __name__ == "__main__":
    main()

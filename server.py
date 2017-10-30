import argparse
import json
import socket

import actions

RECV_BUFFER = 1024


class Server:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.client = None
        self.client_addr = None
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.addr, self.port))
            self.sock.listen()
            print("\nStarting server at http://{}:{}"
                  .format(self.addr, self.port))
        except socket.error as err:
            self.close()
            print("Error:", err)

    def accept(self):
        """ Разрешаем подключиться клиенту """
        if not self.client:
            try:
                self.client, self.client_addr = self.sock.accept()
                print("Запрос на соединение от", self.client_addr)
            except socket.error as err:
                self.client_close()
                print("Error Server.accept():", err)

    def get(self):
        """ Получаем сообщение от клиента """
        if not self.client:
            print("Нет присоединенных клиентов")
            return
        try:
            msg = self.client.recv(RECV_BUFFER)
        except socket.error as err:
            print("Error Server.get():", err)
        return self.parse_msg(msg)

    def parse_msg(self, message):
        """ Парсим сообщение от клиента """
        if message:
            try:
                return json.loads(message.decode("utf-8"))
            except json.JSONDecodeError as err:
                print("Error Server.parse_msg():", err)

    def create_response(self, message):
        """ Формируем ответ клиенту """
        try:
            if message["action"] in actions.actions_list:
                return {"response": 200, "alert": "ok"}
            else:
                return {"response": 400, "error": "неправильный запрос"}
        except (KeyError, TypeError):
            return {"response": 400, "error": "неправильный JSON-объект"}

    def send(self, response):
        """ Отправляем сообщение клиенту """
        if not self.client:
            print("Нет присоединенных клиентов")
            return
        try:
            resp = json.dumps(response)
            self.client.sendall(resp.encode("utf-8"))
            print("Send to", self.client_addr, resp)
        except Exception as err:
            print("Error Server.send():", err)

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


####################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", dest="addr", default="127.0.0.1",
                        help="IP-адрес для прослушивания")
    parser.add_argument("-p", dest="port", type=int, default=7777,
                        help="TCP-порт (по умолчанию 7777)")

    args = parser.parse_args()

    server = Server(args.addr, args.port)

    try:
        while True:
            server.accept()
            msg = server.get()
            if msg:
                print("msg", msg)
                resp = server.create_response(msg)
                server.send(resp)

            # server.client_close()
    except KeyboardInterrupt:
        print("Server close")

    server.close()

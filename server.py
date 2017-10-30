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
        try:
            self.sock = socket.socket(AF_INET, SOCK_STREAM)
            self.sock.bind((self.addr, self.port))
            self.sock.listen()
        except socket.error as err:
            self.close()
            print("Error:", err)
    
    def accept(self):
        """ Разрешаем подключиться клиенту """
        if not self.client:
            try:
                self.client, addr = self.sock.accept()
                print("Запрос на соединение от", addr)
            except socket.error as err:
                self.client_close()
                print("Error Server.accept():", err)

    def get(self):
        """ Получаем сообщение от клиента """
        if not self.client:
            print("Нет присоединенных клиентов")
            return

        msg = b""
        while True:
            try:
                data = self.client.recv(RECV_BUFFER)
            except socket.error as err:
                print("Error Server.get():", err)
            
            if not data:
                break
            msg += data
        return parse_msg(msg)
    
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
                return { "response": 200, "alert": "ok" }
            else:
                return { "response": 400, "error": "неправильный запрос" }
        except (KeyError, TypeError):
            return { "response": 400, "error": "неправильный JSON-объект" }

    def send(self, response):
        """ Отправляем сообщение клиенту """
        if not self.client:
            print("Нет присоединенных клиентов")
            return
        try:
            resp = json.dumps(response)
            self.client.sendall(resp)
        except Exception as err:
            print("Error Server.send():", err)
    
    def client_close(self):
        """ Закрываем соединение с клиентом """
        if self.client:
            self.client.close()
            self client = None

    def close(self):
        """ Закрываем сервер """
        self.client_close()
        if self.sock:
            self.sock.close()
            self.sock = None


####################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", dest="addr", help="IP-адрес для прослушивания")
    parser.add_argument("-p", dest="port", type=int, 
                        help="TCP-порт (по умолчанию 7777)")

    args = parser.parse_args()

    server = Server(args.addr, args.port)

    while True:
        server.accept()
        msg = server.get()
        resp = server.create_response(msg)
        server.send(resp)
        server.close()

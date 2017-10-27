import json
import socket
import sys
import time


BUFFER_SIZE = 1024


class ClientError(Exception):
    """ Класс для ошибок клиента """
    pass


class Client:
    def __init__(self, user, addr="", port=7777, status=""):
        self.user = user
        self.status = status
        self.addr = addr
        self.port = port
        try:
            self.connection = socket.create_connection((addr, port))
        except socket.error as err:
            print("Ошибка соединения:", err)
            self.connection = None
    
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
        try:
            msg = json.dumps(message)
            self.connection.sendall(msg.encode("utf-8"))
        except socket.error as err:
            print("Ошибка отправки сообщения:", err)

    def get_response(self):
        """ Получаем ответ от сервера """
        resp = b""
        while True:
            data = self.connection.recv(BUFFER_SIZE)
            if not data:
                break
            resp += data
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
        print("Client is closed")



def main():
    """ Точка входа """
    argv = sys.argv
    addr = argv[1] if len(argv) > 1 else "127.0.0.1"
    try:
        port = int(argv[2])
    except (ValueError, IndexError):
        port = 7777

    try:
        user = Client("John Doe", addr, port)
        msg = user.create_msg("presence", time.time())
        user.send(msg)

        resp = user.get_response()

        print(user.parse_response(resp))
    
    except Exception as err:
        print("Error:", err)

    finally:
        user.close()


#########################
if __name__ == "__main__":
    main()
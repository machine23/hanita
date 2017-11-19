"""
Здесь собранны инструменты, отвечающие за связь клиента с сервером
"""
import json
import socket

from JIM import JIMMessage

BUFFERSIZE = 1024


###############################################################################
# ### ClientConnectionError
###############################################################################
class ClientConnectionError(Exception):
    """ Базовое исключение для ClientConnection """
    pass


###############################################################################
# ### ClientConnection
###############################################################################
class ClientConnection:
    """
    Класс устанавливает соединение с сервером, передает данные на сервер,
    получает ответ от сервера.
    """

    def __init__(self, host=None, port=7777):
        if host is None:
            host = "127.0.0.1"
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        """ Устанавливаем соединение с сервером """
        if self.connection:
            raise ClientConnectionError("Соединение уже установлено")
        try:
            self.connection = socket.create_connection((self.host, self.port), timeout=0.1)
        except socket.error as err:
            raise ClientConnectionError(err)

    def send(self, message):
        """ Отправляет сообщение на сервер """
        if not isinstance(message, dict):
            raise ClientConnectionError("Неверный формат сообщения")

        json_msg = json.dumps(message)
        byte_msg = json_msg.encode()
        self.connection.sendall(byte_msg)

    def get(self):
        """ Получает сообщение от сервера """
        byte_msg = None
        try:
            byte_msg = self.connection.recv(BUFFERSIZE)
        except socket.timeout:
            pass
        else:
            if byte_msg:
                msg = byte_msg.decode()
                try:
                    json_msg = json.loads(msg)
                except ValueError:
                    # просто отбросить, если пришел не json
                    pass
                else:
                    return JIMMessage(json_msg)

    def close(self):
        """ Закрывает соединение с сервером """
        if self.connection:
            self.connection.close()
            self.connection = None

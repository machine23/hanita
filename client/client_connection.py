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
            self.connection = socket.create_connection((self.host, self.port))
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
        byte_msg = self.connection.recv(BUFFERSIZE)
        if byte_msg:
            json_msg = json.loads(byte_msg)
            return JIMMessage(json_msg)

    def close(self):
        """ Закрывает соединение с сервером """
        if self.connection:
            self.connection.close()
            self.connection = None

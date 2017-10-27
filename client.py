import argparse
import socket
import time


class Client:
    def __init__(self, user, addr="", port=7777, status=""):
        self.user = user
        self.status = status
        self.addr = addr
        self.port = port
    
    def create_msg(self, action, timestamp=None):
        """ Формируем сообщение """
        pass

    def send_msg(self, message):
        """ Отсылаем сообщение на сервер """
        pass

    def get_response(self):
        """ Получаем ответ от сервера """
        pass

    def parse_response(self, resp):
        """ Разбираем ответ от сервера """
        pass

    def close(self):
        """ Закрываем клиент """
        pass
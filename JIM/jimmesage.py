"""
Инструменты для работы с сообщениями по протоколу JIM.
"""
import time

AUTHENTICATE = "authenticate"
QUIT = "quit"
PRESENCE = "presence"
PROBE = "probe"
MSG = "msg"
JOIN = "join"
LEAVE = "leave"


class JIMMesage:
    """ класс, реализует сообщения по протоколу JIM """

    actions = (AUTHENTICATE, QUIT, PRESENCE, PROBE, MSG, JOIN, LEAVE)

    def __init__(self, user_name=None, status=None):
        if user_name is None:
            user_name = "Guest"
        self.name = user_name
        self.status = status

    def authenticate(self, password):
        """ Посылается при аутентификации клиента """
        msg = {
            "action": AUTHENTICATE,
            "time": time.time(),
            "user": {
                "accaunt_name": self.name,
                "password": password
            }
        }
        return msg

    @staticmethod
    def quit():
        """ Посылается при отключении от сервера """
        msg = {
            "action": QUIT,
            "time": time.time()
        }
        return msg

    def presence(self):
        """ Сообщение присутствия """
        msg = {
            "action": PRESENCE,
            "time": time.time(),
            "user": {
                "accaunt_name": self.name,
            }
        }
        if self.status:
            msg["user"]["status"] = self.status
        return msg

    @staticmethod
    def probe():
        """ Сообщение-проверка присутствия """
        msg = {
            "action": PROBE,
            "time": time.time()
        }
        return msg

    def msg(self, to_user, message):
        """ Сообщение пользователю или в чат """
        msg = {
            "action": MSG,
            "time": time.time(),
            "to": to_user,
            "from": self.name,
            "message": message
        }
        return msg

    @staticmethod
    def join(chat_id):
        """ Присоединиться к чату """
        msg = {
            "action": JOIN,
            "time": time.time(),
            "room": chat_id
        }
        return msg

    @staticmethod
    def leave(chat_id):
        """ Покинуть чат """
        msg = {
            "action": LEAVE,
            "time": time.time(),
            "room": chat_id
        }
        return msg

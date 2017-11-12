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


class JIMMessageError(Exception):
    """ класс исключений для JIMMessage """
    pass


class JIMMessage:
    """ класс, реализует сообщения по протоколу JIM """

    actions = (AUTHENTICATE, QUIT, PRESENCE, PROBE, MSG, JOIN, LEAVE)

    def __init__(self, user_name=None, status=None):
        if user_name is None:
            user_name = "Guest"
        self.name = user_name
        self.status = status

    def _base(self, action):
        """
        Создает базовое сообщение с двумя обязательными полями:
        action и time. В случае, если значение параметра action
        отсутствует в списке JIMMessage.actions генерируется
        исключение JIMMessageError.
        """
        if action not in self.actions:
            raise JIMMessageError("wrong action")
        msg = {
            "action": action,
            "time": time.time()
        }
        return msg

    def authenticate(self, password):
        """ Посылается при аутентификации клиента """
        msg = self._base(AUTHENTICATE)
        msg["user"] = {
            "accaunt_name": self.name,
            "password": password
        }
        return msg

    def quit(self):
        """ Посылается при отключении от сервера """
        msg = self._base(QUIT)
        return msg

    def presence(self):
        """ Сообщение присутствия """
        msg = self._base(PRESENCE)
        msg["user"] = {
            "accaunt_name": self.name,
        }
        if self.status:
            msg["user"]["status"] = self.status
        return msg

    def probe(self):
        """ Сообщение-проверка присутствия """
        msg = self._base(PROBE)
        return msg

    def msg(self, to_user, message):
        """ Сообщение пользователю или в чат """
        msg = self._base(MSG)
        msg["to"] = to_user
        msg["from"] = self.name
        msg["message"] = message
        return msg

    def join(self, chat_id):
        """ Присоединиться к чату """
        msg = self._base(JOIN)
        msg["room"] = chat_id
        return msg

    def leave(self, chat_id):
        """ Покинуть чат """
        msg = self._base(LEAVE)
        msg["room"] = chat_id
        return msg

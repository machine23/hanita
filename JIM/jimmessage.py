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

    def authenticate(self, user_name, password):
        """ Посылается при аутентификации клиента """
        msg = self._base(AUTHENTICATE)
        msg["user"] = {
            "accaunt_name": user_name,
            "password": password
        }
        return msg

    def quit(self):
        """ Посылается при отключении от сервера """
        msg = self._base(QUIT)
        return msg

    def presence(self, user_name, status=None):
        """ Сообщение присутствия """
        msg = self._base(PRESENCE)
        msg["user"] = {
            "accaunt_name": user_name,
        }
        if status:
            msg["user"]["status"] = status
        return msg

    def probe(self):
        """ Сообщение-проверка присутствия """
        msg = self._base(PROBE)
        return msg

    def msg(self, user_name, to_user, message):
        """ Сообщение пользователю или в чат """
        msg = self._base(MSG)
        msg["to"] = to_user
        msg["from"] = user_name
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

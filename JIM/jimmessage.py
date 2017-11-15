"""
Инструменты для работы с сообщениями по протоколу JIM.
"""
import time


###############################################################################
# ### JIMMessageError
###############################################################################
class JIMMessageError(Exception):
    """ класс исключений для JIMMessage """
    pass


###############################################################################
# ### JIMResponseError
###############################################################################
class JIMResponseError(Exception):
    """ класс исключений для JIMResponse """
    pass


###############################################################################
# ### JIMMessageAttr
###############################################################################
class JIMMessageAttr:
    """
    Класс-дескриптор, позволяющий обращаться к элементам JIMMessage как
    к атрибутам. Т.е. вместо message['action'] можно писать message.action
    """

    def __init__(self, key):
        self.key = key

    def __get__(self, obj, obj_type):
        return obj.get(self.key, None)

    def __set__(self, obj, value):
        obj.__setitem__(self.key, value)


###############################################################################
# ### JIMMessage
###############################################################################
class JIMMessage(dict):
    """ класс, реализует сообщения по протоколу JIM """
    AUTHENTICATE = "authenticate"
    QUIT = "quit"
    PRESENCE = "presence"
    PROBE = "probe"
    MSG = "msg"
    JOIN = "join"
    LEAVE = "leave"

    actions = (AUTHENTICATE, QUIT, PRESENCE, PROBE, MSG, JOIN, LEAVE)

    action = JIMMessageAttr("action")
    time = JIMMessageAttr("time")
    user = JIMMessageAttr("user")
    to_user = JIMMessageAttr("to")
    from_user = JIMMessageAttr("from")
    message = JIMMessageAttr("message")
    room = JIMMessageAttr("room")

    def __init__(self, action=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = action
        self.time = time.time()

    def authenticate(self, user_name, password):
        """ Посылается при аутентификации клиента """
        msg = JIMMessage(self.AUTHENTICATE)
        msg.user = {
            "accaunt_name": user_name,
            "password": password
        }
        return msg

    def quit(self):
        """ Посылается при отключении от сервера """
        msg = JIMMessage(self.QUIT)
        return msg

    def presence(self, user_name, status=None):
        """ Сообщение присутствия """
        msg = JIMMessage(self.PRESENCE)
        msg.user = {
            "accaunt_name": user_name,
        }
        if status:
            msg.user["status"] = status
        return msg

    def probe(self):
        """ Сообщение-проверка присутствия """
        msg = JIMMessage(self.PROBE)
        return msg

    def msg(self, user_name, to_user, message):
        """ Сообщение пользователю или в чат """
        msg = JIMMessage(self.MSG)
        msg.to_user = to_user
        msg.from_user = user_name
        msg.message = message
        return msg

    def join(self, chat_id):
        """ Присоединиться к чату """
        msg = JIMMessage(self.JOIN)
        msg.room = chat_id
        return msg

    def leave(self, chat_id):
        """ Покинуть чат """
        msg = JIMMessage(self.LEAVE)
        msg.room = chat_id
        return msg


###############################################################################
# ### JIMResponse
###############################################################################
class JIMResponse(dict):
    """ Класс: ответ от сервера """
    status = {
        100: "базовое уведомление",
        101: "важное уведомление",
        200: "ОК",
        201: "объект создан",
        202: "подтверждение",
        400: "неправильный запрос/JSON-объект",
        401: "не авторизован",
        402: "неправильный логин/пароль",
        403: "пользователь заблокирован",
        404: "пользователь/чат отсутствует на сервере",
        409: "уже имеется подключение с указанным логином",
        410: "адресат существует, но недоступен",
        500: "ошибка сервера"
    }

    response = JIMMessageAttr("response")
    time = JIMMessageAttr("time")
    alert = JIMMessageAttr("alert")
    error = JIMMessageAttr("error")

    def __init__(self, code, message=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if code not in self.status:
            raise JIMResponseError("Неверный код ответа")
        self.code = code
        self.time = time.time()
        if code < 400:
            self.alert = message if message else self.status[code]
        else:
            self.error = message if message else self.status[code]

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

    def __init__(self, key, max_len=None):
        self.key = key
        self.max_len = max_len

    def __get__(self, obj, obj_type):
        return obj.get(self.key, None)

    def __set__(self, obj, value):
        if obj.__contains__("action") and self.key == "response":
            raise
        if obj.__contains__("response") and self.key == "action":
            raise
        if isinstance(value, str) and self.max_len:
            if len(value) > self.max_len:
                raise JIMMessageError("Слишком длинное значение")
        obj.__setitem__(self.key, value)


###############################################################################
# ### JIMMessage
###############################################################################
class JIMMessage(dict):
    """ Базовый класс для реализации сообщений/ответов клиент/сервер """
    AUTHENTICATE = "authenticate"
    QUIT = "quit"
    PRESENCE = "presence"
    PROBE = "probe"
    MSG = "msg"
    JOIN = "join"
    LEAVE = "leave"
    GET_CONTACTS = "get_contacts"
    CONTACT_LIST = "contact_list"
    ADD_CONTACT = "add_contact"
    DEL_CONTACT = "del_contact"
    WHO_ONLINE = "who_online"
    ONLINE_LIST = "online_list"

    actions = (AUTHENTICATE, QUIT, PRESENCE, PROBE,
               MSG, JOIN, LEAVE, GET_CONTACTS, CONTACT_LIST,
               ADD_CONTACT, DEL_CONTACT, WHO_ONLINE, ONLINE_LIST)

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
    alert = JIMMessageAttr("alert")
    error = JIMMessageAttr("error")

    action = JIMMessageAttr("action")
    time = JIMMessageAttr("time")
    user = JIMMessageAttr("user")
    to_user = JIMMessageAttr("to")
    from_user = JIMMessageAttr("from")
    message = JIMMessageAttr("message")
    room = JIMMessageAttr("room")
    user_id = JIMMessageAttr("user_id")
    quantity = JIMMessageAttr("quantity")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.action and self.response:
            raise JIMMessageError("Неправильный формат сообщения")


###############################################################################
# ### JIMClientMessage
###############################################################################
class JIMClientMessage(JIMMessage):
    """ Класс сообщения от клиента """

    def __init__(self, action=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = action
        self.time = time.time()

    @staticmethod
    def authenticate(user_name, password):
        """ Посылается при аутентификации клиента """
        msg = JIMClientMessage(JIMMessage.AUTHENTICATE)
        msg.user = {
            "accaunt_name": user_name,
            "password": password
        }
        return msg

    @staticmethod
    def quit():
        """ Посылается при отключении от сервера """
        msg = JIMClientMessage(JIMMessage.QUIT)
        return msg

    @staticmethod
    def presence(user_name, status=None):
        """ Сообщение присутствия """
        msg = JIMClientMessage(JIMMessage.PRESENCE)
        msg.user = {
            "accaunt_name": user_name,
        }
        if status:
            msg.user["status"] = status
        return msg

    @staticmethod
    def probe():
        """ Сообщение-проверка присутствия """
        msg = JIMClientMessage(JIMMessage.PROBE)
        return msg

    @staticmethod
    def msg(user_name, to_user, message):
        """ Сообщение пользователю или в чат """
        msg = JIMClientMessage(JIMMessage.MSG)
        msg.to_user = to_user
        msg.from_user = user_name
        msg.message = message
        return msg

    @staticmethod
    def join(chat_id):
        """ Присоединиться к чату """
        msg = JIMClientMessage(JIMMessage.JOIN)
        msg.room = chat_id
        return msg

    @staticmethod
    def leave(chat_id):
        """ Покинуть чат """
        msg = JIMClientMessage(JIMMessage.LEAVE)
        msg.room = chat_id
        return msg

    @staticmethod
    def get_contacts():
        """ Получить список контактов """
        msg = JIMClientMessage(JIMMessage.GET_CONTACTS)
        return msg

    @staticmethod
    def contact_list(user_id):
        """ Контакт лист """
        msg = JIMClientMessage(JIMMessage.CONTACT_LIST)
        msg.user_id = user_id
        return msg

    @staticmethod
    def add_contact(nickname):
        """ Добавить контакт """
        msg = JIMClientMessage(JIMMessage.ADD_CONTACT)
        msg.user_id = nickname
        return msg

    @staticmethod
    def del_contact(nickname):
        """ Удалить контакт """
        msg = JIMClientMessage(JIMMessage.DEL_CONTACT)
        msg.user_id = nickname
        return msg

    @staticmethod
    def who_online():
        """ Узнать, кто онлайн """
        msg = JIMClientMessage(JIMMessage.WHO_ONLINE)
        return msg

    @staticmethod
    def online_list(user_id):
        """ Онлайн лист """
        msg = JIMClientMessage(JIMMessage.ONLINE_LIST)
        msg.user_id = user_id
        return msg


###############################################################################
# ### JIMResponse
###############################################################################
class JIMResponse(JIMMessage):
    """ Класс: ответ от сервера """

    def __init__(self, code, message=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if code not in self.status:
            raise JIMResponseError("Неверный код ответа")
        self.response = code
        self.time = time.time()
        if code < 400:
            self.alert = message if message else self.status[code]
        else:
            self.error = message if message else self.status[code]

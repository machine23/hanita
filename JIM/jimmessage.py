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
            raise JIMMessageError("action and response in one message")
        if obj.__contains__("response") and self.key == "action":
            raise JIMMessageError("action and response in one message")
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
    chat_id = JIMMessageAttr("chat_id")
    user_id = JIMMessageAttr("user_id")
    message = JIMMessageAttr("message")
    user_status = JIMMessageAttr("user_status")
    password = JIMMessageAttr("password")
    contacts = JIMMessageAttr("contacts")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.action and self.response:
            raise JIMMessageError("Неправильный формат сообщения")

    # def __eq__(self, other):
    #     return self. == other


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
    def authenticate(user_id, password):
        """ Посылается при аутентификации клиента """
        msg = JIMClientMessage(JIMMessage.AUTHENTICATE)
        msg.user_id = user_id
        msg.password = password
        return msg

    @staticmethod
    def quit():
        """ Посылается при отключении от сервера """
        msg = JIMClientMessage(JIMMessage.QUIT)
        return msg

    @staticmethod
    def presence():
        """ Сообщение присутствия """
        msg = JIMClientMessage(JIMMessage.PRESENCE)
        return msg

    @staticmethod
    def probe():
        """ Сообщение-проверка присутствия """
        msg = JIMClientMessage(JIMMessage.PROBE)
        return msg

    @staticmethod
    def msg(user_id, chat_id, message, timestamp=None):
        """ Сообщение пользователю или в чат """
        msg = JIMClientMessage(JIMMessage.MSG)
        msg.user_id = user_id
        msg.chat_id = chat_id
        msg.message = message
        if timestamp:
            msg.time = timestamp
        return msg

    @staticmethod
    def join(chat_id):
        """ Присоединиться к чату """
        msg = JIMClientMessage(JIMMessage.JOIN)
        msg.chat_id = chat_id
        return msg

    @staticmethod
    def leave(chat_id):
        """ Покинуть чат """
        msg = JIMClientMessage(JIMMessage.LEAVE)
        msg.chat_id = chat_id
        return msg

    @staticmethod
    def get_contacts():
        """ Получить список контактов """
        msg = JIMClientMessage(JIMMessage.GET_CONTACTS)
        return msg

    @staticmethod
    def contact_list(contacts=None):
        """
        Контакт лист.
        В этом сообщении передается с сервера список контактов пользователя.
        """
        if contacts is not None and not isinstance(contacts, list):
            raise TypeError("contacts must be list instance")
        msg = JIMClientMessage(JIMMessage.CONTACT_LIST)
        msg.contacts = contacts or []
        return msg

    @staticmethod
    def add_contact(user_id):
        """
        Сообщение на сервер с заданием добавить пользователя с user_id в
        список контактов.
        """
        msg = JIMClientMessage(JIMMessage.ADD_CONTACT)
        msg.user_id = user_id
        return msg

    @staticmethod
    def del_contact(contact_id):
        """ Удалить контакт """
        msg = JIMClientMessage(JIMMessage.DEL_CONTACT)
        msg.user_id = contact_id
        return msg

    @staticmethod
    def who_online():
        """ Узнать, кто онлайн """
        msg = JIMClientMessage(JIMMessage.WHO_ONLINE)
        return msg

    # @staticmethod
    # def online_list(user_id):
    #     """ Онлайн лист """
    #     msg = JIMClientMessage(JIMMessage.ONLINE_LIST)
    #     msg.user_id = user_id
    #     return msg


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

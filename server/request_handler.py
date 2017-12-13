import socketserver
import socket
import json
import time
import threading
from .models import *
from .server_db import ServerDB
from JIM import JIMMessage, JIMResponse, JIMClientMessage

RECV_BUFFER = 1024


###############################################################################
# ### ClientRequestHandler
###############################################################################
class ClientRequestHandler(socketserver.BaseRequestHandler):
    """ Класс-обработчик запросов клиента """

    def setup(self):
        # yapf: disable
        self.action_handlers = {
            JIMMessage.MSG: self.handler_msg,
            JIMMessage.QUIT: self.handler_quit,
            JIMMessage.AUTHENTICATE: self.handler_authenticate,
            JIMMessage.PRESENCE: self.handler_presence,
            # JIMMessage.WHO_ONLINE: self.handler_who_online,
            JIMMessage.GET_CONTACTS: self.handler_get_contacts,
            JIMMessage.ADD_CONTACT: self.handler_add_contact,
            JIMMessage.NEW_CHAT: self.handler_new_chat
        }
        # yapf: enable
        self.__quit = False
        self.msg = None
        self.user = None
        self.db = ServerDB(self.server.base, "sqlite:///server.db")
        self.lock = threading.Lock()

    def handle(self):
        """ Основной обработчик """
        while not self.__quit:
            msgs = self.get()
            if msgs:
                for msg in msgs:
                    print("server handle msg:", msg)
                    if self.__quit:
                        break
                    if msg.action and msg.action in self.action_handlers:
                        self.msg = msg
                        action_handler = self.action_handlers[msg.action]
                        resp = action_handler()
                        self.send(resp)
                        self.msg = None
                    else:
                        self.send(JIMResponse(400))
    
    def finish(self):
        self.db.set_user_online(self.user.id, False)
        self.db.close()

    def response(self, resp_code=None):
        """ Ответить на сообщение """
        if resp_code:
            self.send(JIMResponse(resp_code))

    def send_to_all(self, chat_id, message):
        """ Отправить сообщение всем авторизованным пользователям чата. """
        online_users = self.db.get_online_users(chat_id)
        print("send_to_all online_users:", online_users)
        for user in online_users:
            self.send_to(user, message)
        return JIMResponse(200)

    def get(self):
        """ Получить сообщение от ... """
        _get_data = True
        bmsg = b""
        while _get_data:
            try:
                data = self.request.recv(RECV_BUFFER)
            except ConnectionError:
                self.__quit = True
                break
            if data == b"" or data.decode().endswith("}"):
                _get_data = False
            bmsg += data
        if bmsg:
            messages_str = bmsg.decode().replace("}{", "}<split>{")
            arr_msgstr = messages_str.split("<split>")
            msgs = [JIMMessage(json.loads(msg)) for msg in arr_msgstr]
            return msgs

    def send_to(self, user, message):
        """ Отправить сообщение другому клиенту """
        json_msg = json.dumps(message)
        bmsg = json_msg.encode("utf_8")
        with socket.fromfd(user.fileno, socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                print("send_to:", s, bmsg)
                s.sendall(bmsg)
            except socket.error:
                self.db.set_user_online(user.id, False)
                return JIMResponse(410)
        return JIMResponse(200)

    def send(self, message):
        """ Ответить отправителю """
        msg = json.dumps(message).encode()
        try:
            self.request.sendall(msg)
        except ConnectionError:
            self.__quit = True

    # handlers ################################################################

    def handler_authenticate(self):
        """
        Аутентификация пользователя.
        Возвращает код ответа.
        """
        if self.msg.action != JIMMessage.AUTHENTICATE:
            raise
        if self.msg.user and set(
                self.msg.user) == {"login", "password"}:
            login = self.msg.user["login"]
            password = self.msg.user["password"]
            user = User(login)
            # Если пользователя нет в базе
            user_id = self.db.get_user_id(login)
            if user_id is None:
                self.db.add_obj(user)
                print("user.id:", user.id)
            else:
                user = self.db.get_obj(User, user_id)
            print(user_id)
            print(user)
            self.user = user
            self.db.set_user_online(user.id, True, self.request.fileno())
            # Проверка, имеется ли уже подключение с данным ID
            # elif self.user_online(user.user_name):
                # Добавить проверку, если уже имеется подключение с данным ID,
                # то это подключение еще актуально (отправить PROBE)
                # return 409
            # Прошли все проверки, добавляем юсера в онлайн
            # self.db.save_hist(user, time.time(), str(
                # self.client_address))
            self.server.clients[self.request] = user.id
            user_info = {"user_id": user.id, "user_name": user.name}
            # self.user_name = user.user_name
            response = JIMResponse(200, user=user_info)
            ####### Вынести в другую функцию ##################################
            user_chats = self.db.get_chats_for(self.user.id)
            for chat in user_chats:
                info_msg = self.get_chat_info(chat.id)
                self.send(info_msg)
            ###################################################################
            print(response)
            return response
        return JIMResponse(400)

    def handler_quit(self):
        """ Обработчик события Quit """
        if self.msg.action != JIMMessage.QUIT:
            raise

        self.__quit = True
        return JIMResponse(200)

    def handler_msg(self):
        """ Обработчик события MSG """
        if self.msg.action != JIMMessage.MSG:
            raise
        print("handler_msg self.msg:", self.msg)
        msg = ChatMsg(self.user.id, self.msg.chat_id, self.msg.timestamp,
                      self.msg.message)
        self.db.add_obj(msg)
        out_msg = self.msg
        out_msg.msg_id = msg.id
        out_msg.user = {
            "user_id": self.user.id,
            "user_name": self.user.name
        }
        print("handler_msg out_msg:", out_msg)
        self.send_to_all(msg.chat_id, out_msg)
        return JIMResponse(200)

    def handler_presence(self):
        """ Обработчик события Presence """
        if self.msg.action != JIMMessage.PRESENCE:
            raise
        return JIMResponse(200)




    def handler_get_contacts(self):
        """ Обработчик события Who online  """
        # users_list = self.db.get_contacts(self.user_name)
        # contacts = [obj.contact_id for obj in users_list]
        # num = len(contacts)
        # resp = JIMResponse(202)
        # resp.quantity = num
        # self.send(resp)
        # for contact in contacts:
        #     contact_name = self.db.get_user_name(contact)
        #     msg = JIMClientMessage.contact_list(contact_name)
        #     self.send(msg)
        return JIMResponse(200)

    def handler_add_contact(self):
        """ Обработчик события ADD_CONTACT """
        print("handler_add_contact msg:", self.msg)
        contact_name = self.msg["user_name"]
        contact_id = self.db.get_user_id(contact_name)
        if not contact_id:
            # упрощение, просто добавит нового пользователя
            user = self.db.add_new_user(contact_name)
            contact_id = user.id
        self.db.add_contact(self.user.id, contact_id)
        contact = {"user_id":contact_id, "user_name":contact_name}
        msg = JIMClientMessage.contact_list([contact])
        self.send(msg)
        return JIMResponse(202)


    def handler_new_chat(self):
        """ Обработчик события new_chat """
        chat_name = self.msg["chat_name"]
        chat_user_ids = self.msg["chat_user_ids"]
        print("create new chat", chat_name, "with", )
        chat = self.db.add_new_chat(chat_name)
        print("self.user.id:", self.user.id)
        self.db.add_user_to_chat(chat.id, self.user.id)
        for user_id in chat_user_ids:
            self.db.add_user_to_chat(chat.id, user_id)
        msg = self.get_chat_info(chat.id)
        self.send_to_all(chat.id, msg)
        return JIMResponse(202)

    def get_chat_info(self, chat_id):
        chat = self.db.get_chat(chat_id)
        users = self.db.get_users_for(chat.id)
        chat_users = []
        for user in users:
            chat_user = {"user_id": user.id, "user_name": user.name}
            chat_users.append(chat_user)
        print(chat_users)
        msg = JIMClientMessage.chat_info(chat.id, chat.name, chat_users)
        return msg


import socketserver
import socket
import json
import time
import threading
from .models import User
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
            JIMMessage.WHO_ONLINE: self.handler_who_online,
            JIMMessage.GET_CONTACTS: self.handler_get_contacts,
            JIMMessage.ADD_CONTACT: self.handler_add_contact
        }
        # yapf: enable
        self.__quit = False
        self.msg = None
        self.user_name = None
        self.db = ServerDB(self.server.base, "sqlite:///users.db")
        self.lock = threading.Lock()

    def handle(self):
        """ Основной обработчик """
        while not self.__quit:
            msgs = self.get()
            if msgs:
                for msg in msgs:
                    if self.__quit:
                        break
                    if msg.action and msg.action in self.action_handlers:
                        self.msg = msg
                        action_handler = self.action_handlers[msg.action]
                        resp = action_handler()
                        self.response(resp)
                        self.msg = None
                    else:
                        self.response(400)
    
    def finish(self):
        self.db.close()

    def response(self, resp_code=None):
        """ Ответить на сообщение """
        if resp_code:
            self.send(JIMResponse(resp_code))

    def send_to_all(self):
        """ Отправить сообщение всем авторизованным пользователям """
        clients = [n for n in self.server.clients]
        for client in clients:
            if self.server.clients[client] and client is not self.request:
                self.send_to(client, self.msg)
        return 200

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

    def send_to(self, client, message):
        """ Отправить сообщение другому клиенту """
        json_msg = json.dumps(message)
        bmsg = json_msg.encode("utf_8")
        try:
            client.sendall(bmsg)
        except socket.error:
            return 410
        return 200

    def send(self, message):
        """ Ответить отправителю """
        msg = json.dumps(message).encode()
        try:
            self.request.sendall(msg)
        except ConnectionError:
            self.__quit = True

    def handler_authenticate(self):
        """
        Аутентификация пользователя.
        Возвращает код ответа.
        """
        if self.msg.action != JIMMessage.AUTHENTICATE:
            raise
        if self.msg.user and set(
                self.msg.user) == {"accaunt_name", "password"}:
            accaunt_name = self.msg.user["accaunt_name"]
            password = self.msg.user["password"]
            user = User(accaunt_name, password)
            # Если пользователя нет в базе
            if not self.db.exists(user.user_name):
                self.db.add_new_user(user)
            # Проверка, имеется ли уже подключение с данным ID
            elif self.user_online(user.user_name):
                # Добавить проверку, если уже имеется подключение с данным ID,
                # то это подключение еще актуально (отправить PROBE)
                return 409
            # Прошли все проверки, добавляем юсера в онлайн
            self.db.save_hist(user, time.time(), str(
                self.client_address))
            self.server.clients[self.request] = user.user_name
            self.user_name = user.user_name
            return 200
        return 400

    def handler_quit(self):
        """ Обработчик события Quit """
        if self.msg.action != JIMMessage.QUIT:
            raise

        self.__quit = True
        return 200

    def handler_msg(self):
        """ Обработчик события MSG """
        if self.msg.action != JIMMessage.MSG:
            raise
        if not (self.msg.to_user or isinstance(self.msg.to_user, str)):
            return 400
        if self.msg.to_user.startswith("#"):
            return self.send_to_all()  # Пока отправляем всем
        else:
            username = self.msg.to_user
            if self.user_online(username):
                user_sock = self.get_client_by_id(username)
                resp = self.send_to(user_sock, self.msg)
                return resp
            if self.db.exists(username):
                return 410
            return 404

    def handler_presence(self):
        """ Обработчик события Presence """
        if self.msg.action != JIMMessage.PRESENCE:
            raise
        return 200

    def user_online(self, user_id):
        """ проверить, есть ли такой пользователь онлайн """
        return user_id in self.server.clients.values()

    def get_client_by_id(self, user_id):
        """ Получить сокет клиента по его ID """
        for sock, id_ in self.server.clients.items():
            if id_ == user_id:
                return sock

    def handler_who_online(self):
        """ Обработчик события Who online """
        clients = [i for i in self.server.clients if self.server.clients[i]]
        num = len(clients)
        resp = JIMResponse(202)
        resp.quantity = num
        self.send(resp)
        for _id in clients:
            msg = JIMClientMessage.online_list(self.server.clients[_id])
            self.send(msg)
        return 200

    def handler_get_contacts(self):
        """ Обработчик события Who online  """
        users_list = self.db.get_contacts(self.user_name)
        contacts = [obj.contact_id for obj in users_list]
        num = len(contacts)
        resp = JIMResponse(202)
        resp.quantity = num
        self.send(resp)
        for contact in contacts:
            contact_name = self.db.get_user_name(contact)
            msg = JIMClientMessage.contact_list(contact_name)
            self.send(msg)
        return 200

    def handler_add_contact(self):
        """ Обработчик события ADD_CONTACT """
        contact = self.msg.user_id
        if self.db.exists(contact):
            self.db.add_contact(self.user_name, contact)
            return 202
        return 404

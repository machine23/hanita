import socketserver
import socket
import json
import time
from .models import User
from JIM import JIMMessage, JIMResponse, JIMClientMessage

RECV_BUFFER = 1024


###############################################################################
# ### ClientRequestHandler
###############################################################################
class ClientRequestHandler(socketserver.BaseRequestHandler):
    """ Класс-обработчик запросов клиента """

    def setup(self):
        self.action_handlers = {
            JIMMessage.MSG: self.handler_msg,
            JIMMessage.QUIT: self.handler_quit,
            JIMMessage.AUTHENTICATE: self.handler_authenticate,
            JIMMessage.PRESENCE: self.handler_presence,
            JIMMessage.WHO_ONLINE: self.handler_who_online,
            JIMMessage.GET_CONTACTS: self.handler_get_contacts,
            JIMMessage.ADD_CONTACT: self.handler_add_contact
        }
        self.__quit = False
        self.msg = None
        self.user_id = None

    def handle(self):
        """ Основной обработчик """
        while not self.__quit:
            msg = self.get()
            if msg and msg.action and msg.action in self.action_handlers:
                self.msg = msg
                action_handler = self.action_handlers[msg.action]
                resp = action_handler()
                print(resp)
                self.response(resp)
                self.msg = None
            else:
                self.response(400)

    def response(self, resp_code=None):
        """ Ответить на сообщение """
        if resp_code:
            self.send(JIMResponse(resp_code))

    def send_to_all(self):
        """ Отправить сообщение всем авторизованным пользователям """
        for client in self.server.clients:
            if self.server.clients[client] and client is not self.request:
                self.send_to(client, self.msg)
        return 200

    def get(self):
        """ Получить сообщение от ... """
        bmsg = self.request.recv(RECV_BUFFER)
        if bmsg:
            msg = JIMMessage(json.loads(bmsg))
            print(msg)
            return msg

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
        self.request.sendall(json.dumps(message).encode())

    def handler_authenticate(self):
        """
        Аутентификация пользователя.
        Возвращает код ответа.
        """
        if self.msg.action != JIMMessage.AUTHENTICATE:
            raise
        if self.msg.user and set(self.msg.user) == {"accaunt_name", "password"}:
            accaunt_name = self.msg.user["accaunt_name"]
            password = self.msg.user["password"]
            user = User(accaunt_name, password)
            # Если пользователя нет в базе
            if not self.server.db.exists(user.user_id):
                self.server.db.add_new_user(user)
            # Проверка, имеется ли уже подключение с данным ID
            elif self.user_online(user.user_id):
                # Добавить проверку, если уже имеется подключение с данным ID,
                # то это подключение еще актуально (отправить PROBE)
                return 409
            # Прошли все проверки, добавляем юсера в онлайн
            self.server.db.save_hist(
                user, time.time(), str(self.client_address))
            self.server.clients[self.request] = user.user_id
            self.user_id = user.user_id
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
            if self.server.db.exists(username):
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
        users_list = self.server.db.get_contacts(self.user_id)
        contacts = [obj.contact_id for obj in users_list]
        num = len(contacts)
        resp = JIMResponse(202)
        resp.quantity = num
        self.send(resp)
        for user_id in contacts:
            msg = JIMClientMessage.contact_list(user_id)
            self.send(msg)
        return 200

    def handler_add_contact(self):
        """ Обработчик события ADD_CONTACT """
        contact = self.msg.user_id
        if self.server.db.exists(contact):
            self.server.db.add_contact(self.user_id, contact)
            return 202
        return 404

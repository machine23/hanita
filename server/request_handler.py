import socketserver
import json
import time
from .models import User
from JIM import JIMMessage, JIMResponse

RECV_BUFFER = 1024


###############################################################################
# ### ClientRequestHandler
###############################################################################
class ClientRequestHandler(socketserver.BaseRequestHandler):
    """ Класс-обработчик запросов клиента """


    def setup(self):
        self.action_handlers = {
            JIMMessage.MSG          : self.handler_msg,
            JIMMessage.QUIT         : self.handler_quit,
            JIMMessage.AUTHENTICATE : self.handler_authenticate,
            JIMMessage.PRESENCE     : self.handler_presence
        }
        self.__quit = False
        self.msg = None

    def handle(self):
        """ Основной обработчик """
        while not self.__quit:
            msg = self.get()
            if msg and msg.action and msg.action in self.action_handlers:
                self.msg = msg
                action_handler = self.action_handlers[msg.action]
                resp = action_handler()
                self.response(resp)
                self.msg = None

    def response(self, resp_code=None):
        """ Ответить на сообщение """
        if resp_code:
            print(resp_code)
            self.send(JIMResponse(resp_code))

    def send_to_all(self):
        """ Отправить сообщение всем авторизованным пользователям """
        print("send_to_all", self.server.clients)
        for client in self.server.clients:
            if self.server.clients[client] and client is not self.request:
                print("send_to", self.msg)
                self.send_to(client, self.msg)

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
        client.sendall(bmsg)

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
            # Проверка, имеется ли уже подключение с данным ID
            if user.user_id in self.server.clients.values():
                return 409
            # Проверка пользователя в базе
            if not self.server.db.exists(user):
                self.server.db.add_new_user(user)
            self.server.db.save_hist(user, time, self.client_address)
            self.server.clients[self.request] = user.user_id
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
        self.send_to_all()
        return 200

    def handler_presence(self):
        """ Обработчик события Presence """
        if self.msg.action != JIMMessage.PRESENCE:
            raise
        return 200

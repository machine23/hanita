import socketserver
import json
from JIM import JIMMessage, JIMResponse

RECV_BUFFER = 1024


###############################################################################
# ### ClientRequestHandler
###############################################################################
class ClientRequestHandler(socketserver.BaseRequestHandler):
    """ Класс-обработчик запросов клиента """

    def handle(self):
        """ Основной метод-обработчик """
        while True:
            msg = self.get_from(self.request)
            if msg and msg.action:
                if msg.action == msg.MSG:
                    for client in self.server.clients:
                        if client is not self.request:
                            self.send_to(client, msg)
                elif msg.action == msg.QUIT:
                    break

    def get_from(self, from_):
        """ Получить сообщение от ... """
        bmsg = from_.recv(RECV_BUFFER)
        if bmsg:
            msg = JIMMessage(json.loads(bmsg))
            print(msg)
            self.send_to(from_, JIMResponse(200))
            return msg

    def send_to(self, client, message):
        """ Отправить сообщение """
        json_msg = json.dumps(message)
        bmsg = json_msg.encode("utf_8")
        client.sendall(bmsg)

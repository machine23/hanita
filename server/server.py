""" server.py """
import argparse
# import functools
import json
# import logging
import select
import socket
import socketserver
import sys

# from utils import log_config
from JIM import JIMMessage, JIMResponse

RECV_BUFFER = 1024

# logger = logging.getLogger("server.main")


# def log(func):
#     @functools.wraps(func)
#     def inner(*args, **kwargs):
#         msg = ", ".join(str(item) for item in args) if args else ""
#         if kwargs:
#             s_kwargs = ", ".join(
#                 "{}={}".format(k, v) for k, v in kwargs.items()
#             )
#             msg += (", " if msg else "") + s_kwargs
#         name = func.__name__
#         logger.info("%s (%s)", name, msg)
#         return func(*args, **kwargs)
#     return inner


class ServerError(Exception):
    """ класс для ошибок сервера """
    pass


###############################################################################
# Server
###############################################################################
class Server(socketserver.ThreadingTCPServer):
    """ class Server """
    clients = []
    allow_reuse_address = True

    def get_request(self):
        """ Получаем запрос """
        request, client_address = self.socket.accept()
        self.clients.append(request)
        print("get_request")
        return request, client_address

    def verify_request(self, request, client_address):
        """
        Проверяем запрос
        Return True if we should proceed with this request
        """
        print("verify_request", request, client_address)
        return True

    def close_request(self, request):
        print("close_request")
        self.clients.remove(request)
        request.close()

    # def process_request(self, request, client_address):
    #     print("process_request")
    #     self.finish_request(request, client_address)


###############################################################################
# ### ClientRequestHandler
###############################################################################
class ClientRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
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
        bmsg = from_.recv(RECV_BUFFER)
        if bmsg:
            msg = JIMMessage(json.loads(bmsg))
            print(msg)
            self.send_to(from_, JIMResponse(200))
            return msg

    def send_to(self, client, message):
        json_msg = json.dumps(message)
        bmsg = json_msg.encode("utf_8")
        client.sendall(bmsg)


###############################################################################
# read_args
###############################################################################
def read_args():
    """ Читаем аргументы командной строки """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        dest="addr",
        default="127.0.0.1",
        help="IP-адрес для прослушивания"
    )
    parser.add_argument(
        "-p",
        dest="port",
        type=int,
        default=7777,
        help="TCP-порт (по умолчанию 7777)"
    )

    args = parser.parse_args()
    return args


###############################################################################
# main
###############################################################################
def main():
    """ mainloop """
    args = read_args()

    with Server((args.addr, args.port), ClientRequestHandler) as server:
        server_addr = server.socket.getsockname()
        serve_message = "Serving on {host} port {port} ..."
        print(serve_message.format(host=server_addr[0], port=server_addr[1]))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


###############################################################################
#
###############################################################################
if __name__ == "__main__":
    main()

""" server.py """
import argparse
import socketserver
import sys
from .server_db import ServerDB
from .models import Base

from .request_handler import ClientRequestHandler


###############################################################################
# Server
###############################################################################
class Server(socketserver.ThreadingTCPServer):
    """ class Server """
    clients = {}
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, database: ServerDB,
                 bind_and_activate=True):
        socketserver.ThreadingTCPServer.__init__(
            self, server_address, RequestHandlerClass, bind_and_activate)
        self.db = database

    def get_request(self):
        """ Получаем запрос """
        request, client_address = self.socket.accept()
        self.clients[request] = None
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
        self.clients.pop(request, None)
        request.close()


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

    sdb = ServerDB(Base, "sqlite:///server.db")

    with Server((args.addr, args.port), ClientRequestHandler, sdb) as server:
        server_addr = server.socket.getsockname()
        serve_message = "Serving on {host} port {port} ..."
        print(serve_message.format(host=server_addr[0], port=server_addr[1]))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

    print("\nKeyboard interrupt received, exiting.")
    sdb.close()
    sys.exit(0)


###############################################################################
#
###############################################################################
if __name__ == "__main__":
    main()

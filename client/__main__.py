import argparse
import sys
from .client_connection import ClientConnection
from .client_qtview import QtClientView
from .client_db import ClientDB
from .client import Client
from .client_view import ConsoleClientView


###############################################################################
# read_args
###############################################################################
def read_args():
    """
    Получаем аргументы командной строки.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "addr",
        default="127.0.0.1",
        nargs="?",
        help="IP сервера (по умолчанию 127.0.0.1)")
    parser.add_argument(
        "port",
        type=int,
        default=7777,
        nargs="?",
        help="TCP-порт сервера (по умолчанию 7777)")
    parser.add_argument(
        "-r",
        dest="read",
        action="store_true",
        help="определяет режим работы на получение сообщений")
    parser.add_argument(
        "-w",
        dest="write",
        action="store_true",
        help="включает режим отправки сообщений")

    args = parser.parse_args()
    if args.read and args.write:
        print("Пожалуйста, определите режим работы:",
              "\n\t-w на отправку сообщений", "\n\t-r на получение сообщений")
        sys.exit(0)
    return args


###############################################################################
# main
###############################################################################
def main():
    """ Точка входа """
    args = read_args()
    if args.write:
        mode = "write"
    elif args.read:
        mode = "read"
    else:
        mode = None

    connection = ClientConnection(args.addr, args.port)

    model = ClientDB("client.db")

    if mode == "read":
        client = Client(connection, model, ConsoleClientView)
    elif mode == "write":
        client = Client(connection, model, QtClientView)
    else:
        sys.exit()
    client.run(mode)

    client.close("Good Bye!")


###############################################################################
if __name__ == "__main__":
    main()

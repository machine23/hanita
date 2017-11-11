import socket
import pytest

from client import ClientConnection, ClientConnectionError


class MySocket:
    """ заглушка для socket.socket """

    def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
        self.data = None
        self.addr = None

    def sendall(self, data):
        self.data = data

    def recv(self, buffersize):
        return b'{"action": "test"}'

    def create_connection(self, address):
        if isinstance(address, tuple) \
                and len(address) == 2 \
                and isinstance(address[0], str) \
                and isinstance(address[1], int):
            self.addr = address
            return self
        else:
            raise socket.error

    def close(self):
        self.data = None
        self.addr = None


@pytest.fixture
def connection():
    conn = ClientConnection()
    yield conn
    conn.close()


@pytest.fixture
def socket_mock():
    orig_conn = socket.create_connection
    socket.create_connection = MySocket
    yield
    socket.create_connection = orig_conn


def test_connect(connection, socket_mock):
    pass


def test_send(connection, socket_mock):
    pass


def test_get(connection, socket_mock):
    pass


def test_close(connection, socket_mock):
    pass

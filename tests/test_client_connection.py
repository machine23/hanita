import socket
import pytest

from client import ClientConnection, ClientConnectionError


class MySocket:
    """ заглушка для socket.socket """

    def __init__(self,
                 sock_type=socket.AF_INET,
                 sock_family=socket.SOCK_STREAM,
                 timeout=None):
        self.data = None
        self.addr = None

    def sendall(self, data):
        self.data = data

    def recv(self, buffersize):
        return b'{"action": "test"}'

    def create_connection(self, address, timeout=None):
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
def socket_mock():
    orig_conn = socket.create_connection
    socket.create_connection = MySocket
    yield
    socket.create_connection = orig_conn


@pytest.fixture
def conn(socket_mock):
    conn = ClientConnection()
    yield conn
    conn.close()


def test_connect(conn):
    assert conn.connection == None
    conn.connect()
    assert isinstance(conn.connection, MySocket)
    with pytest.raises(ClientConnectionError):
        conn.connect()


def test_send(conn):
    conn.connect()
    conn.send({"a": "b"})
    assert conn.connection.data == b'{"a": "b"}'
    with pytest.raises(ClientConnectionError):
        conn.send("bad message")


def test_get(conn):
    conn.connect()
    assert conn.get() == {"action": "test"}


def test_close(conn):
    conn.connect()
    conn.close()
    assert conn.connection is None

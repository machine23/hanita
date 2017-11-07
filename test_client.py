import json
import socket

import pytest

import actions
from client import Client, ClientError


@pytest.fixture
def client():
    client = Client("John")
    yield client
    return client


class MySocket:
    """ заглушка для socket.socket """

    def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
        self.data = b""
        self.addr = None

    def send(self, data):
        self.data = data
        return len(data)

    def sendall(self, data):
        self.data = data

    def recv(self, buffersize):
        return b'{"response":200}'

    def connect(self, address):
        if isinstance(address, tuple) \
                and len(address) == 2 \
                and isinstance(address[0], str) \
                and isinstance(address[1], int):
            self.addr = address
        else:
            raise socket.error

    def close(self):
        self.data = b""
        self.addr = None


@pytest.fixture
def my_socket():
    orig_socket = socket.socket
    socket.socket = MySocket
    yield
    socket.socket = orig_socket


def test_create_message(client):
    with pytest.raises(ClientError):
        client.create_message("bad action")

    expected = {
        "action": actions.PRESENCE,
        "time": 1,
        "type": "status",
        "user": {
            "account_name": "John",
            "status": None
        }
    }
    assert expected == client.create_message(actions.PRESENCE, timestamp=1)
    expected = {
        "action": actions.MSG,
        "time": 1,
        "to": "Mike",
        "from": "John",
        "encoding": "ascii",
        "message": "hello"
    }
    assert expected == client.create_message(
        actions.MSG, to_user="Mike", message="hello", timestamp=1)


def test_parse_response(client):
    resp = b'{"response":200,"time":1,"alert":"ok"}'
    expected = {
        "response": 200,
        "time": 1,
        "alert": "ok"
    }
    assert client.parse_response(resp) == expected


def test_close(client):
    client.close()
    assert client.connection is None


def test_connect(client, my_socket):
    client.connect("127.0.0.1")
    assert client.connection.addr == ("127.0.0.1", 7777)
    with pytest.raises(ClientError):
        client.connect()
    client.close()
    with pytest.raises(ClientError):
        client.connect(127001, 8080)


def test_send(client, my_socket):
    client.close()
    with pytest.raises(ClientError):
        client.send("hello")
    client.connect()
    expected = b'{"a": "b"}'
    client.send({"a": "b"})
    assert expected == client.connection.data


def test_get(client, my_socket, monkeypatch):
    client.close()
    with pytest.raises(ClientError):
        client.get()
    client.connect()
    expected = {"response": 200}
    assert expected == client.get()
    monkeypatch.setattr(client.connection, "recv", lambda x: None)
    with pytest.raises(ClientError):
        client.get()

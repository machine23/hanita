import pytest
from client import Client


@pytest.fixture(scope="module")
def client():
    client = Client("John")
    yield client
    return client


def test_create_msg(client):
    assert client.create_msg("a", 1) == {
        "action": "a",
        "time": 1,
        "type": "status",
        "user": {
            "account_name": "John",
            "status": ""
        }
    }


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


### Тесты, которые нужно заполнить в будущем ###
def test_connect(client):
    pass


def test_send(client):
    assert True


def test_get_response(client):
    assert True

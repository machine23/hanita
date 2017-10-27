import pytest
from client import Client


@pytest.fixture(scope="module")
def client(request):
    print("Create Client")
    client = Client("John")
    def teardown():
        print("Close Client")
        client.close()
    request.addfinalizer(teardown)
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


def test_send(client):
    assert True


def test_get_response(client):
    assert True


def test_parse_response(client):
    assert True
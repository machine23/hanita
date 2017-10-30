import pytest

from server import Server
import actions


@pytest.yield_fixture
def server():
    s = Server("127.0.0.1", 8888)
    yield s
    s.close()


def test_parse_msg(server):
    expected = {"action": "test", "time": 1}
    bmsg = b'{"action":"test","time":1}'
    assert server.parse_msg(bmsg) == expected


def test_create_response_ok(server):
    expected = {"response": 200, "alert": "ok"}
    msg = {"action": actions.PRESENCE, "time": 1}
    assert server.create_response(msg) == expected


def test_create_response_wrong_msg(server):
    expected = {"response": 400, "error": "неправильный запрос"}
    msg = {"action": "wrong action"}
    assert server.create_response(msg) == expected


def test_create_response_wrong_json(server):
    expected = {"response": 400, "error": "неправильный JSON-объект"}
    msg = "this is not json"
    assert server.create_response(msg) == expected

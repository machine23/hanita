""" Тесты для JIMMessage """
import pytest
import time

from JIM import JIMMessage, JIMMessageError


@pytest.fixture
def message():
    return JIMMessage()


class TestJIMMessage:
    def test_authenticate(self, message):
        expect = {
            "action": "authenticate",
            "time": time.time(),
            "user": {
                "accaunt_name": "John",
                "password": "abc"
            }
        }
        result = message.authenticate("John", "abc")
        assert expect.keys() == result.keys()
        assert expect["action"] == result["action"]
        assert expect["user"] == result["user"]
        assert abs(expect["time"] - result["time"]) < 0.1

    def test_quit(self, message):
        expect = {
            "action": "quit",
            "time": time.time()
        }
        result = message.quit()
        assert expect.keys() == result.keys()
        assert expect["action"] == result["action"]
        assert abs(expect["time"] - result["time"]) < 0.1

    def test_presence(self, message):
        expect = {
            "action": "presence",
            "time": time.time(),
            "user": {
                "accaunt_name": "John",
                "status": "busy"
            }
        }
        result = message.presence("John", "busy")
        assert expect.keys() == result.keys()
        assert expect["action"] == result["action"]
        assert expect["user"] == result["user"]
        assert abs(expect["time"] - result["time"]) < 0.1

    def test_probe(self, message):
        expect = {
            "action": "probe",
            "time": time.time()
        }
        result = message.probe()
        assert expect.keys() == result.keys()
        assert expect["action"] == result["action"]
        assert abs(expect["time"] - result["time"]) < 0.1

    def test_msg(self, message):
        expect = {
            "action": "msg",
            "time": time.time(),
            "to": "Maria",
            "from": "John",
            "message": "Hello"
        }
        result = message.msg("John", "Maria", "Hello")
        assert expect.keys() == result.keys()
        assert expect["action"] == result["action"]
        assert abs(expect["time"] - result["time"]) < 0.1
        assert expect["to"] == result["to"]
        assert expect["from"] == result["from"]
        assert expect["message"] == result["message"]

    def test_join(self, message):
        expect = {
            "action": "join",
            "time": time.time(),
            "room": "#all"
        }
        result = message.join("#all")
        assert expect.keys() == result.keys()
        assert expect["action"] == result["action"]
        assert abs(expect["time"] - result["time"]) < 0.1
        assert expect["room"] == result["room"]

    def test_leave(self, message):
        expect = {
            "action": "leave",
            "time": time.time(),
            "room": "#all"
        }
        result = message.leave("#all")
        assert expect.keys() == result.keys()
        assert expect["action"] == result["action"]
        assert abs(expect["time"] - result["time"]) < 0.1
        assert expect["room"] == result["room"]

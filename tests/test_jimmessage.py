""" Тесты для JIMMessage """
import pytest
import time

from JIM import JIMMessage, JIMClientMessage, JIMMessageError, JIMMessageAttr


def check_message(expect, result):
    assert isinstance(expect, dict)
    assert isinstance(result, JIMMessage)
    assert result.keys() == expect.keys()
    for key in expect:
        if key == "timestamp":
            assert abs(result.timestamp - expect["timestamp"]) < 0.1
        else:
            assert expect[key] == result[key]


def test_JIMMessageAttr():
    class Msg(dict):
        attr = JIMMessageAttr("attr", 8)
        action = JIMMessageAttr("action")
        response = JIMMessageAttr("response")

    msg = Msg()
    msg.attr = "12345678"
    assert msg.attr == "12345678"
    assert msg["attr"] == "12345678"
    msg.attr = 123
    assert msg.attr == 123
    with pytest.raises(JIMMessageError):
        msg.attr = "123456789"
    with pytest.raises(JIMMessageError):
        msg.action = "a"
        msg.response = 200
    with pytest.raises(JIMMessageError):
        msg = Msg()
        msg.response = 200
        msg.action = "a"


class TestJIMMessage:
    def test_authenticate(self):
        expect = {
            "action": "authenticate",
            "timestamp": time.time(),
            "user_id": 123,
            "password": "abc"
        }
        result = JIMClientMessage.authenticate(123, "abc")
        check_message(expect, result)

    def test_quit(self):
        expect = {
            "action": "quit",
            "timestamp": time.time()
        }
        result = JIMClientMessage.quit()
        check_message(expect, result)

    def test_presence(self):
        expect = {
            "action": "presence",
            "timestamp": time.time(),
        }
        result = JIMClientMessage.presence()
        check_message(expect, result)

    def test_probe(self):
        expect = {
            "action": "probe",
            "timestamp": time.time()
        }
        result = JIMClientMessage.probe()
        check_message(expect, result)

    def test_msg(self):
        expect = {
            "action": "msg",
            "timestamp": time.time(),
            "user_id": "John",
            "chat_id": "#all",
            "message": "Hello"
        }
        result = JIMClientMessage.msg("John", "#all", "Hello")
        check_message(expect, result)

    def test_join(self):
        expect = {
            "action": "join",
            "timestamp": time.time(),
            "chat_id": "#all"
        }
        result = JIMClientMessage.join("#all")
        check_message(expect, result)

    def test_leave(self):
        expect = {
            "action": "leave",
            "timestamp": time.time(),
            "chat_id": "#all"
        }
        result = JIMClientMessage.leave("#all")
        check_message(expect, result)

    def test_get_contacts(self):
        expect = {
            "action": "get_contacts",
            "timestamp": time.time()
        }
        result = JIMClientMessage.get_contacts()
        check_message(expect, result)

    def test_contact_list(self):
        expect = {
            "action": "contact_list",
            "timestamp": time.time(),
            "contacts": []
        }
        result = JIMClientMessage.contact_list()
        check_message(expect, result)
        with pytest.raises(TypeError):
            JIMClientMessage.contact_list("")

    def test_add_contact(self):
        expect = {
            "action": "add_contact",
            "timestamp": time.time(),
            "user_id": 123
        }
        result = JIMClientMessage.add_contact(123)
        check_message(expect, result)

    def test_del_contact(self):
        expect = {
            "action": "del_contact",
            "timestamp": time.time(),
            "user_id": 123
        }
        result = JIMClientMessage.del_contact(123)
        check_message(expect, result)

    def test_who_online(self):
        expect = {
            "action": "who_online",
            "timestamp": time.time(),
        }
        result = JIMClientMessage.who_online()
        check_message(expect, result)

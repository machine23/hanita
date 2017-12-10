import pytest
import sqlite3
import time

from JIM import JIMClientMessage, JIMMessage

from client import ClientDB, ClientDBError


@pytest.fixture
def db():
    client_db = ClientDB()

    cmd_user = "INSERT INTO users(user_id, user_name) VALUES (?, ?)"
    client_db.cursor.execute(cmd_user, (1, "user1"))
    client_db.conn.commit()

    cmd_chat = "INSERT INTO chats(chat_id, chat_name) VALUES (?, ?)"
    client_db.cursor.execute(cmd_chat, (1, "chat1"))
    client_db.conn.commit()

    # cmd_chat_user = "INSERT INTO chat_users(user_id, chat_id) VALUES (?, ?)"
    # client_db.cursor.execute(cmd_chat_user, (1, 1))
    # client_db.cursor.execute(cmd_chat_user, (2, 1))
    # client_db.cursor.execute(cmd_chat_user, (1, 2))
    # client_db.conn.commit()

    msg1 = JIMClientMessage.msg(1, 1, "Hello", 3.3)
    # msg2 = JIMClientMessage.msg(2, 1, "Hi")
    # msg3 = JIMClientMessage.msg(1, 2, "Good!")

    data1 = (1, msg1.user_id, msg1.chat_id, msg1.timestamp, msg1.message)
    # data2 = (msg2.from_user, msg2.to_user, msg2.time, msg2.message)
    # data3 = (msg3.from_user, msg3.to_user, msg3.time, msg3.message)

    cmd = """INSERT INTO messages(msg_id, user_id, chat_id, time, message)
             VALUES (?, ?, ?, ?, ?)"""
    # for data in [data1, data2, data3]:
    client_db.cursor.execute(cmd, data1)
    client_db.conn.commit()
    yield client_db
    client_db.close()


def test_user_exists(db):
    assert db.user_exists("1")
    assert not db.user_exists("5")


def test_add_user(db):
    db.add_user(4, "user4")
    assert db.user_exists(4)
    with pytest.raises(ClientDBError):
        db.add_user(4, "user5")


def test_get_user(db):
    assert db.get_user(1) == {"user_id": 1, "user_name": "user1"}
    assert db.get_user(5) == {}


def test_update_user(db):
    db.update_user(1, "updated_name")
    assert db.get_user(1)["user_name"] == "updated_name"
    db.update_user(1, "another_name")
    assert db.get_user(1)["user_name"] == "another_name"
    db.update_user(5, "user5")
    assert db.get_user(5) == {"user_id": 5, "user_name": "user5"}


def test_chat_exists(db):
    assert db.chat_exists(1)
    assert not db.chat_exists(5)


def test_get_chats(db):
    result = db.get_chats()
    expect = ["chat" + str(i) for i in range(3)]
    assert result == expect


def test_add_chat(db):
    db.add_chat(2, "new_chat")
    assert db.chat_exists(2)
    with pytest.raises(ClientDBError):
        db.add_chat(2, "another_chat")


def test_get_chat(db):
    expect = {
        "chat_id": 1,
        "chat_name": "chat1",
        "read_time": None
    }
    assert db.get_chat(1) == expect
    assert db.get_chat(5) == {}


def test_set_chat_readed(db):
    db.set_chat_readed(1)
    assert time.time() - db.get_chat(1)["read_time"] < 0.1


def test_del_chat(db):
    db.del_chat(1)
    assert db.chat_exists(1) is False
    db.del_chat(1)


def test_get_chats(db):
    assert db.get_chats() == [1]
    db.add_chat(2, "chat2")
    assert db.get_chats() == [1, 2]
    for i in db.get_chats():
        db.del_chat(i)
    assert db.get_chats() == []


def test_msg_exists(db):
    assert db.msg_exists(1) is True
    assert db.msg_exists(2) is False

def test_add_msg(db):
    msg2 = JIMClientMessage.msg(1, 1, "Hello", 1.1)
    msg2.msg_id = 2
    db.add_msg(**msg2)
    assert db.msg_exists(2)

def test_get_msg(db):
    expect = {
        "msg_id": 1,
        "user_id": 1,
        "chat_id": 1,
        "timestamp": 3.3,
        "message": "Hello",
        "readed": 0
    }
    assert db.get_msg(1) == expect
    assert db.get_msg(2) == {}

def test_get_msgs(db):
    msgs = db.get_msgs(1)
    assert msgs == [1]
    db.add_msg(5, 1, 1, 5.5, "message")
    assert db.get_msgs(1) == [1, 5]
    db.del_chat(1)
    assert db.get_msgs(1) == []

###############################################################################
def test_get_chat_users(db):
    assert db.get_chat_users("chat0") == ["1", "2"]
    assert db.get_chat_users("chat1") == ["1"]
    assert db.get_chat_users("chat2") == []
    assert db.get_chat_users("no_chat") == []


def test_add_chat_user(db):
    assert "3" not in db.get_chat_users("chat0")
    db.add_chat_user("3", "chat0")
    assert "3" in db.get_chat_users("chat0")
    with pytest.raises(ClientDBError):
        assert db.add_chat_user("3", "chat0")
    with pytest.raises(ClientDBError):
        db.add_chat_user("unknown", "chat0")
    with pytest.raises(ClientDBError):
        db.add_chat_user("1", "no_chat")


def test_get_messages(db):
    assert len(db.get_messages("chat0")) == 2
    assert len(db.get_messages("chat1")) == 1
    assert len(db.get_messages("chat2")) == 0
    for msg in db.get_messages("chat0"):
        assert isinstance(msg, JIMMessage)
        assert set(msg.keys()) == {"action", "from", "to", "time", "message"}


def test_add_message(db):
    before = len(db.get_messages("chat0"))
    msg = JIMClientMessage.msg("1", "chat0", "check it")
    db.add_message(msg)
    assert len(db.get_messages("chat0")) - before == 1
    assert msg in db.get_messages("chat0")

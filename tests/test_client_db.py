import pytest
import sqlite3

from JIM import JIMClientMessage, JIMMessage

from client import ClientDB, ClientDBError


@pytest.fixture
def db():
    client_db = ClientDB()
    cmd_user = "INSERT INTO users(user_name) VALUES (?)"
    for name in ["1", "2", "3"]:
        client_db.cursor.execute(cmd_user, (name, ))
    client_db.conn.commit()

    cmd_chat = "INSERT INTO chats(chat_name) VALUES (?)"
    for chat in ["chat" + str(i) for i in range(3)]:
        client_db.cursor.execute(cmd_chat, (chat, ))
    client_db.conn.commit()

    cmd_chat_user = "INSERT INTO chat_users(user_id, chat_id) VALUES (?, ?)"
    client_db.cursor.execute(cmd_chat_user, (1, 1))
    client_db.cursor.execute(cmd_chat_user, (2, 1))
    client_db.cursor.execute(cmd_chat_user, (1, 2))
    client_db.conn.commit()

    msg1 = JIMClientMessage.msg(1, 1, "Hello")
    msg2 = JIMClientMessage.msg(2, 1, "Hi")
    msg3 = JIMClientMessage.msg(1, 2, "Good!")

    data1 = (msg1.from_user, msg1.to_user, msg1.time, msg1.message)
    data2 = (msg2.from_user, msg2.to_user, msg2.time, msg2.message)
    data3 = (msg3.from_user, msg3.to_user, msg3.time, msg3.message)

    cmd = """INSERT INTO messages(creator_id, chat_id, time, message)
             VALUES (?, ?, ?, ?)"""
    for data in [data1, data2, data3]:
        client_db.cursor.execute(cmd, data)
    client_db.conn.commit()
    yield client_db
    client_db.close()


def test_get_users(db):
    result = db.get_users()
    assert isinstance(result, list)
    assert len(result) == 3
    assert ["1", "2", "3"] == result


def test_add_user(db):
    db.add_user("4")
    assert "4" in db.get_users()


def test_get_user_id(db):
    assert db.get_user_id("1") == 1
    assert db.get_user_id("4") is None


def test_get_user_name(db):
    assert db.get_user_name(1) == "1"
    assert db.get_user_name(2) == "2"
    assert db.get_user_name(3) == "3"
    assert db.get_user_name(4) is None


def test_user_exists(db):
    assert db.user_exists("1")
    assert not db.user_exists("5")


def test_get_chats(db):
    result = db.get_chats()
    expect = ["chat" + str(i) for i in range(3)]
    assert result == expect


def test_add_chat(db):
    db.add_chat("new_chat")
    assert "new_chat" in db.get_chats()


def test_chat_exists(db):
    assert db.chat_exists("chat1")
    assert not db.chat_exists("no_chat")


def test_get_chat_id(db):
    assert db.get_chat_id("chat0") == 1
    assert db.get_chat_id("chat1") == 2
    assert db.get_chat_id("no_chat") is None


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

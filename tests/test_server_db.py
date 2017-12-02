import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server import ServerDB, ServerDBError, ServerDBUnknownID, Base
from server import User, Chat, ChatUser, ChatMsg, Contact


@pytest.fixture
def db():
    server_db = ServerDB(Base)

    server_db.session.add(User("user1"))
    server_db.session.add(User("user2"))
    server_db.session.add(User("user3"))
    server_db.session.commit()
    users = server_db.session.query(User).all()
    print(users)

    server_db.session.add(Contact(1, 2))
    server_db.session.add(Contact(1, 3))
    server_db.session.add(Contact(2, 3))
    server_db.session.commit()

    server_db.session.add(Chat("chat1"))
    server_db.session.add(Chat("chat2"))
    server_db.session.add(Chat("chat3"))
    server_db.session.commit()

    # В chat1 - 2 users, chat2 - 1 user, chat3 - 0 users
    # user1 has 2 chats, user2 has 1 chat, user3 has 0 chat
    server_db.session.add(ChatUser(1, 1))
    server_db.session.add(ChatUser(1, 2))
    server_db.session.add(ChatUser(2, 1))
    server_db.session.commit()

    yield server_db

    server_db.session.rollback()
    server_db.close()


def test_get_obj(db):
    user = db.get_obj(User, 1)
    assert isinstance(user, User)
    assert user.id == 1
    assert user.name == str(1)
    user = db.get_obj(User, 5)
    assert user is None


def test_user_exists(db):
    assert db.obj_exists(User, 1)
    assert db.obj_exists(User, 2)
    assert db.obj_exists(User, 3)
    assert not db.obj_exists(User, 4)


def test_add_user(db):
    assert not db.obj_exists(User, 4)
    db.add_obj(User("Petr"))
    assert db.obj_exists(User, 4)


def test_del_obj(db):
    assert db.obj_exists(User, 1)
    user_before = db.get_obj(User, 1)
    assert user_before.status == "active"
    db.del_obj(user_before)
    user_after = db.get_obj(User, 1)
    assert user_after.status == "deleted"

def test_get_active_chatusers(db):
    assert len(db.get_active_chatusers(1)) == 2
    assert len(db.get_active_chatusers(2)) == 1
    assert len(db.get_active_chatusers(3)) == 0
    assert len(db.get_active_chatusers(4)) == 0
    users = db.get_active_chatusers(1)
    assert all(isinstance(i, User) for i in users)
    assert users[0].name == "user1"
    assert users[1].name == "user2"

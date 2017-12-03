import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server import ServerDB, ServerDBError, SDBChatEmptyError, Base
from server import User, Chat, ChatUser, ChatMsg, Contact
from JIM import JIMClientMessage


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

    # msg1 = JIMClientMessage.msg()
    # Перейти в сообщениях с name на ID !!!!!!!!!!!!!!!!!!!

    yield server_db

    server_db.session.rollback()
    server_db.close()


def test_get_obj(db):
    user = db.get_obj(User, 1)
    assert isinstance(user, User)
    assert user.id == 1
    assert user.name == "user1"
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
    user_before = db.get_obj(User, 1)
    assert user_before.status == "active"
    db.del_obj(User, user_before.id)
    user_after = db.get_obj(User, 1)
    assert user_after.status == "deleted"
    with pytest.raises(SDBChatEmptyError):
        db.del_obj(Chat, 1)


def test_get_chat_users(db):
    assert len(db.get_chat_users(1)) == 2
    assert len(db.get_chat_users(2)) == 1
    assert not db.get_chat_users(3)
    assert not db.get_chat_users(4)
    # Проверка, что выдает список только User-ов
    users = db.get_chat_users(1)
    assert all(isinstance(i, User) for i in users)
    assert users[0].name == "user1"
    assert users[1].name == "user2"
    # Проверка, что выдает список только активных User-ов
    db.del_obj(User, users[0].id)
    users = db.get_chat_users(1)
    assert len(users) == 1
    assert users[0].name == "user2"
    # Проверка, что выдает список User-ов, если они активные ChatUser-ы
    db.del_obj(ChatUser, 2)
    users = db.get_chat_users(1)
    assert len(users) == 0


def test_get_chats_for(db: ServerDB):
    assert len(db.get_chats_for(1)) == 2
    assert len(db.get_chats_for(2)) == 1
    assert len(db.get_chats_for(3)) == 0
    assert len(db.get_chats_for(4)) == 0
    # Проверка, что выдает список только Chat-ов
    chats = db.get_chats_for(1)
    assert all(isinstance(c, Chat) for c in chats)
    assert chats[0].name == "chat1"
    assert chats[1].name == "chat2"


def test_get_chats_for_active_chatuser_only(db):
    # Проверка, что выдает список Chat-ов, если user активный ChatUser
    db.del_obj(ChatUser, 3)
    chats = db.get_chats_for(1)
    assert len(chats) == 1
    assert chats[0].name == "chat1"


def test_add_user_to_chat(db: ServerDB):
    db.add_user_to_chat(1, 3)
    users = db.get_chat_users(1)
    assert len(users) == 3
    assert users[2].name == "user3"
    with pytest.raises(ServerDBError):
        db.add_user_to_chat(1, 4)
    with pytest.raises(ServerDBError):
        db.add_user_to_chat(4, 1)
    with pytest.raises(ServerDBError):
        db.add_user_to_chat(1, 1)


def test_del_user_from_chat(db: ServerDB):
    db.del_user_from_chat(1, 2)
    users = db.get_chat_users(1)
    assert len(users) == 1
    assert users[0].name == "user1"


def test_find_users(db):
    assert len(db.find_users("u")) == 3
    assert len(db.find_users("1")) == 1
    assert len(db.find_users("4")) == 0


def test_get_user_contacts(db):
    assert len(db.get_user_contacts(1)) == 2
    assert len(db.get_user_contacts(2)) == 1
    assert not db.get_user_contacts(3)
    assert not db.get_user_contacts(4)
    contacts = db.get_user_contacts(1)
    assert all(isinstance(c, User) for c in contacts)
    assert contacts[0].name == "user2"
    assert contacts[1].name == "user3"
    db.del_contact(1, 3)
    assert len(db.get_user_contacts(1)) == 1


def test_del_contact(db):
    db.del_contact(1, 2)
    assert len(db.get_user_contacts(1)) == 1
    db.del_contact(1, 3)
    assert not db.get_user_contacts(1)

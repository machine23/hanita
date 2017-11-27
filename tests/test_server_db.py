import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server import ServerDB, ServerDBError, ServerDBUnknownID, Base
from server import User, UserHistory, UserContact


@pytest.fixture
def db():
    server_db = ServerDB(Base)

    server_db.session.add(User("1"))
    server_db.session.add(User("2"))
    server_db.session.add(User("3"))
    server_db.session.commit()

    server_db.session.add(UserContact("1", "2"))
    server_db.session.add(UserContact("1", "3"))
    server_db.session.add(UserContact("2", "3"))
    server_db.session.commit()

    yield server_db

    server_db.session.rollback()
    server_db.close()


def test_get_user(db):
    user1 = db.get_user("1")
    user2 = db.get_user("2")
    assert isinstance(user1, User)
    assert user1.user_id == "1"
    assert isinstance(user2, User)
    assert user2.user_id == "2"
    user_none = db.get_user("None")
    assert user_none is None


def test_exists(db):
    assert db.exists("1")
    assert db.exists("2")
    assert db.exists("3")
    assert not db.exists("4")


def test_add_new_user(db):
    assert not db.exists("4")
    db.add_new_user(User("4"))
    assert db.exists("4")


def test_get_contacts(db):
    contacts_3 = db.get_contacts("3")
    assert len(contacts_3) == 0
    contacts_2 = db.get_contacts("2")
    assert len(contacts_2) == 1
    contacts_1 = db.get_contacts("1")
    assert len(contacts_1) == 2
    with pytest.raises(ServerDBUnknownID):
        db.get_contacts("4")


def test_add_contact(db):
    before = len(db.get_contacts("3"))
    db.add_contact("3", "1")
    after = len(db.get_contacts("3"))
    assert after - before == 1


def test_del_contact(db):
    before = len(db.get_contacts("1"))
    db.del_contact("1", "3")
    after = len(db.get_contacts("1"))
    assert before - after == 1
    with pytest.raises(ServerDBUnknownID):
        db.del_contact("4", "1")
    with pytest.raises(ServerDBUnknownID):
        db.del_contact("1", "4")
    with pytest.raises(ServerDBError):
        db.del_contact("3", "1")


def test_del_user(db):
    with pytest.raises(ServerDBUnknownID):
        db.del_user("4")
    with pytest.raises(ServerDBError):
        db.del_user("3")
    db.add_new_user(User("4"))
    db.del_user("4")
    assert not db.exists("4")

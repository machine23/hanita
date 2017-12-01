import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server import ServerDB, ServerDBError, ServerDBUnknownID, Base
from server import User


@pytest.fixture
def db():
    server_db = ServerDB(Base)

    server_db.session.add(User("1"))
    server_db.session.add(User("2"))
    server_db.session.add(User("3"))
    server_db.session.commit()
    users = server_db.session.query(User).all()
    print(users)

    # server_db.session.add(UserContact("1", "2"))
    # server_db.session.add(UserContact("1", "3"))
    # server_db.session.add(UserContact("2", "3"))
    # server_db.session.commit()

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


def test_del_user(db):
    assert db.obj_exists(User, 1)
    user = db.get_obj(User, 1)
    db.del_obj(user)
    assert not db.obj_exists(User, 1)

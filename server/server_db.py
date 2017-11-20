from sqlalchemy import create_engine
from sqlalchemy import MetaData, Integer, String, Table, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event

from .models import User, UserHistory, UserContact, Base


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


###############################################################################
# ### ServerDBError
###############################################################################
class ServerDBError(Exception):
    """ Класс-исключение для ServerDB """
    pass


###############################################################################
# ### class ServerDB
###############################################################################
class ServerDB:
    def __init__(self, base):
        self.engine = create_engine("sqlite:///users.db", echo=True,
                                    connect_args={"check_same_thread":False})
        self.base = base
        self.session = None
        try:
            self.setup()
        except:
            self.close()

    def _add(self, obj, error_msg):
        """ Добавить в базу """
        try:
            self.session.add(obj)
            self.session.commit()
        except:
            self.session.rollback()
            raise ServerDBError(error_msg)

    def add_new_user(self, user):
        """ Добавить нового пользователя в БД """
        self._add(user, "ServerDB.add_new_user error")

    def exists(self, user):
        """ Проверить наличие пользователя в БД """
        q = self.session.query(User).filter(User.user_id == user.user_id)
        return self.session.query(q.exists()).scalar()

    def save_hist(self, user, time, ip):
        """ Сохранить историю пользователя в БД """
        s = UserHistory(user, time, ip)
        self._add(s, "ServerDB.save_hist error")

    def add_contact(self, user, contact):
        """ Добавить контакт """
        s = UserContact(user, contact)
        self._add(s, "ServerDB.add_contact error")

    def get_contacts(self, user):
        """ Получить контакты """
        out = self.session.query(UserContact).filter(
            UserContact.user_id == user.user_id).all()
        return out

    def setup(self):
        """ Загрузка БД """
        self.base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close(self):
        """ Закрытие БД """
        if self.session:
            self.session.close()
            self.session = None

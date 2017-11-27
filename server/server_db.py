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


class ServerDBUnknownID(Exception):
    """ Исключение при неверном ID """
    pass


###############################################################################
# ### class ServerDB
###############################################################################


class ServerDB:
    """ Класс для управления БД сервера """

    def __init__(self, base, dbname=""):
        if not dbname:
            dbname = "sqlite:///:memory:"
        self.engine = create_engine(
            dbname, echo=False, connect_args={
                "check_same_thread": False
            })
        self.base = base
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

    def get_user(self, user_name):
        """ Получить пользователя по ID """
        if self.exists(user_name):
            user = self.session.query(User).filter(
                User.user_name == user_name).first()
            return user

    def get_id(self, user_name):
        """ Получить id по имени """
        if self.exists(user_name):
            user = self.get_user(user_name)
            return user.user_id

    def get_user_name(self, user_id):
        """ Получить имя по id """
        user = self.session.query(User).filter(User.user_id == user_id).first()
        return user.user_name

    def exists(self, user_name):
        """ Проверить наличие пользователя в БД """
        q = self.session.query(User).filter(User.user_name == user_name)
        return self.session.query(q.exists()).scalar()

    def exists_id(self, user_id):
        """ Проверить наличие пользователя в БД """
        q = self.session.query(User).filter(User.user_id == user_id)
        return self.session.query(q.exists()).scalar()

    def save_hist(self, user_id, time, ip):
        """ Сохранить историю пользователя в БД """
        s = UserHistory(user_id, time, ip)
        self._add(s, "ServerDB.save_hist error")

    def add_contact(self, user_name, contact_name):
        """ Добавить контакт """
        user_id = self.get_id(user_name)
        contact_id = self.get_id(contact_name)
        s = UserContact(user_id, contact_id)
        self._add(s, "ServerDB.add_contact error")

    def get_contacts(self, user_name):
        """ Получить контакты """
        if self.exists(user_name):
            user_id = self.get_id(user_name)
            out = self.session.query(UserContact).filter(
                UserContact.user_id == user_id).all()
            return out
        raise ServerDBUnknownID("unknown user")

    def del_contact(self, user_name, contact_name):
        """ Удалить контакт для пользователя """
        if not self.exists(contact_name):
            raise ServerDBUnknownID("unknown contact_name")
        if not self.exists(user_name):
            raise ServerDBUnknownID("unknown user_name")
        user_id = self.get_id(user_name)
        contact_id = self.get_id(contact_name)
        user_contact = self.session.query(UserContact).filter(
            UserContact.user_id == user_id).filter(
                UserContact.contact_id == contact_id).first()
        try:
            self.session.delete(user_contact)
            self.session.commit()
        except:
            self.session.rollback()
            raise ServerDBError("ServerDB.del_contact err")

    def del_user(self, user_id):
        """ Удалить пользователя из БД """
        if self.exists(user_id):
            user = self.session.query(User).filter(
                User.user_id == user_id).first()
            try:
                self.session.delete(user)
                self.session.commit()
            except:
                self.session.rollback()
                raise ServerDBError("ServerDB.del_user error")
        else:
            raise ServerDBUnknownID("unknown user_id")

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

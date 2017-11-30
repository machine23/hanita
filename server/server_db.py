from sqlalchemy import create_engine
from sqlalchemy import MetaData, Integer, String, Table, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event

from .models import User, Contact, Base


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
            dbname, echo=True, connect_args={
                "check_same_thread": False
            })
        self.base = base
        self.session = None
        try:
            self.setup()
        except Exception as err:
            print(str(err))
            self.close()

    def _add(self, obj, error_msg):
        """ Добавить в базу """
        try:
            self.session.add(obj)
            self.session.commit()
        except:
            self.session.rollback()
            raise ServerDBError(error_msg)

    def add_user(self, user):
        """ Добавить нового пользователя в БД """
        self._add(user, "ServerDB.add_user error")

    def get_user(self, user_name):
        """ Получить пользователя по ID """
        pass
    #     if self.exists(user_name):
    #         user = self.session.query(User).filter(
    #             User.user_name == user_name).first()
    #         return user

    def get_id(self, user_name):
        """ Получить id по имени """
        pass
    #     if self.exists(user_name):
    #         user = self.get_user(user_name)
    #         return user.id

    def get_user_name(self, id_user):
        """ Получить имя по id """
        pass
    #     user = self.session.query(User).filter(User.id_user == id_user).first()
    #     return user.name

    def exists(self, user_name):
        """ Проверить наличие пользователя в БД """
        pass
    #     q = self.session.query(User).filter(User.user_name == user_name)
    #     return self.session.query(q.exists()).scalar()

    def exists_id(self, id_user):
        """ Проверить наличие пользователя в БД """
        pass
    #     q = self.session.query(User).filter(User.id_user == id_user)
    #     return self.session.query(q.exists()).scalar()

    def add_contact(self, user_name, contact_name):
        """ Добавить контакт """
        pass
    #     id_user = self.get_id(user_name)
    #     contact_id = self.get_id(contact_name)
    #     s = Contact(id_user, contact_id)
    #     self._add(s, "ServerDB.add_contact error")

    def get_contacts(self, user_name):
        """ Получить контакты """
        pass
    #     if self.exists(user_name):
    #         id_user = self.get_id(user_name)
    #         out = self.session.query(Contact).filter(
    #             Contact.id_user == id_user).all()
    #         return out
    #     raise ServerDBUnknownID("unknown user")

    def del_contact(self, user_name, contact_name):
        """ Удалить контакт для пользователя """
        pass
    #     if not self.exists(contact_name):
    #         raise ServerDBUnknownID("unknown contact_name")
    #     if not self.exists(user_name):
    #         raise ServerDBUnknownID("unknown user_name")
    #     id_user = self.get_id(user_name)
    #     contact_id = self.get_id(contact_name)l_user(self, id_user):
    #     user_contact = self.session.query(Contact).filter(
    #         Contact.id_user == id_user).filter(
    #             Contact.id == contact_id).first()
    #     try:
    #         self.session.delete(user_contact)
    #         self.session.commit()
    #     except:
    #         self.session.rollback()
    #         raise ServerDBError("ServerDB.del_contact err")

    def del_user(self, id_user):
        """ Удалить пользователя из БД """
        pass
    #     if self.exists(id_user):
    #         user = self.session.query(User).filter(
    #             User.id == id_user).first()
    #         try:
    #             self.session.delete(user)
    #             self.session.commit()
    #         except:
    #             self.session.rollback()
    #             raise ServerDBError("ServerDB.del_user error")
    #     else:
    #         raise ServerDBUnknownID("unknown id_user")

    def setup(self):
        """ Загрузка БД """
        self.base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.session.commit()

    def close(self):
        """ Закрытие БД """
        print("DB close")
        if self.session:
            self.session.close()
            self.session = None

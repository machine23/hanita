from sqlalchemy import create_engine
from sqlalchemy import MetaData, Integer, String, Table, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event

from .models import User, Chat, ChatUser, ChatMsg, Contact, Base


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
    """ Класс для управления БД сервера

    """

    def __init__(self, base, dbname=""):
        if not dbname:
            dbname = "sqlite:///:memory:"
        self.engine = create_engine(
            dbname, echo=False, connect_args={
                "check_same_thread": False
            })
        self.base = base
        self.session = None
        try:
            self.setup()
        except Exception as err:
            print(str(err))
            self.close()

    def add_obj(self, obj, error_msg="add_obj error"):
        """ Добавить в базу """
        try:
            self.session.add(obj)
            self.session.commit()
        except:
            self.session.rollback()
            raise ServerDBError(error_msg)

    def get_obj(self, cls, _id):
        """ Получить из базы """
        obj = self.session.query(cls).filter(cls.id == _id).first()
        return obj

    def del_obj(self, obj, error_msg="del_obj error"):
        """ Удалить из базы.
        Ничего из базы не удаляется. Меняется только статус с active на deleted
        """
        try:
            obj.status = "deleted"
            self.session.commit()
        except:
            self.session.rollback()
            raise ServerDBError(error_msg)

    def obj_exists(self, cls, _id):
        """ Проверить наличие в базе """
        q = self.session.query(cls).filter(cls.id == _id)
        return self.session.query(q.exists()).scalar()

    def get_active_chatusers(self, chat_id):
        """ Получить список всех активных пользователей чата """
        user_list = self.session.query(User) \
            .join(ChatUser) \
            .filter(ChatUser.chat_id == chat_id) \
            .filter(ChatUser.status == "active").all()
        return user_list

    def get_active_chats_for(self, user_id):
        """ Получить список всех активных чатов для данного пользователя """
        chat_list = self.session.query(Chat) \
            .join(ChatUser) \
            .filter(ChatUser.user_id == user_id).all()
        return chat_list

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

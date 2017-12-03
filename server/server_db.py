from sqlalchemy import create_engine
from sqlalchemy import MetaData, Integer, String, Table, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event

from .models import User, Chat, ChatUser, ChatMsg, Contact, Base
from JIM import JIMClientMessage


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


class SDBChatEmptyError(ServerDBError):
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

    def get_obj(self, cls, obj_id):
        """ Получить из базы """
        obj = self.session.query(cls).filter(cls.id == obj_id).first()
        return obj

    def del_obj(self, cls, obj_id, error_msg="del_obj error"):
        """ Удалить из базы.
        Ничего из базы не удаляется. Меняется только статус с active на deleted
        """
        obj = self.session.query(cls) \
            .filter(cls.id == obj_id) \
            .first()
        if cls == Chat and self.get_chat_users(obj.id):
            raise SDBChatEmptyError(
                "Попытка удалить чат с активными пользователями")
        try:
            obj.status = "deleted"
            self.session.commit()
        except:
            self.session.rollback()
            raise ServerDBError(error_msg)

    def obj_exists(self, cls, obj_id):
        """ Проверить наличие в базе """
        q = self.session.query(cls).filter(cls.id == obj_id)
        return self.session.query(q.exists()).scalar()

    def get_chat_users(self, chat_id):
        """ Получить список всех активных пользователей чата """
        user_list = self.session.query(User) \
            .join(ChatUser) \
            .filter(ChatUser.chat_id == chat_id) \
            .filter(ChatUser.status == "active") \
            .filter(User.status == "active").all()
        return user_list

    def get_chats_for(self, user_id):
        """ Получить список всех активных чатов для данного пользователя """
        chat_list = self.session.query(Chat) \
            .join(ChatUser) \
            .filter(ChatUser.user_id == user_id) \
            .filter(ChatUser.status == "active").all()
        return chat_list

    def add_user_to_chat(self, chat_id, user_id):
        """ Добавить пользователя в чат """
        chatuser = ChatUser(chat_id, user_id)
        self.add_obj(chatuser)

    def del_user_from_chat(self, chat_id, user_id):
        """ Удалить пользователя из чата """
        chatuser = self.session.query(ChatUser) \
            .filter(ChatUser.chat_id == chat_id) \
            .filter(ChatUser.user_id == user_id) \
            .first()
        if chatuser:
            self.del_obj(ChatUser, chatuser.id)

    def find_users(self, substr):
        """ Найти всех пользователей по строке поиска"""
        users = self.session.query(User) \
            .filter(User.name.like('%{}%'.format(substr))) \
            .all()
        return users

    def get_user_contacts(self, user_id):
        """ Получить список контактов пользователя """
        contacts = self.session.query(User) \
            .join(Contact, User.id == Contact.contact_id) \
            .filter(Contact.user_id == user_id) \
            .filter(Contact.status == "active") \
            .all()
        return contacts

    def del_contact(self, user_id, contact_id):
        contact = self.session.query(Contact) \
            .filter(Contact.user_id == user_id) \
            .filter(Contact.contact_id == contact_id) \
            .first()
        self.del_obj(Contact, contact.id)

    def get_chat_msgs(self, chat_id):
        """ Получить сообщения для чата """
        msgs = self.session.query(ChatMsg) \
            .filter(ChatMsg.chat_id == chat_id) \
            .all()
        jim_msgs = [
            JIMClientMessage.msg(m.user_id, m.chat_id, m.message, m.time)
            for m in msgs
        ]
        return jim_msgs


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

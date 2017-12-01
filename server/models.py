from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text, UniqueConstraint

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    name = Column(String(25))

    def __init__(self, name, password=""):
        self.name = name
        # self.password = password

    def __repr__(self):
        return "User (userid = {}, name = {})".format(
            self.id, self.name)


class Chat(Base):
    __tablename__ = "chats"
    id = Column("id", Integer, primary_key=True)
    name = Column(String)


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Chat <{}, {}>".format(self.id, self.name)


class ChatUser(Base):
    __tablename__ = "chat_users"
    id = Column("id", Integer, primary_key=True)
    id_chat = Column(Integer, ForeignKey("chats.id"))
    id_user = Column(Integer, ForeignKey("users.id"))
    __uix = UniqueConstraint(id_chat, id_user)


    def __init__(self, id_chat, id_user):
        self.id_chat = id_chat
        self.id_user = id_user

    def __repr__(self):
        return "ChatUser {}".format(self.id)


class ChatMsg(Base):
    __tablename__ = "chat_msgs"
    id = Column("id", Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    id_chat = Column(Integer, ForeignKey("chats.id"))
    time = Column(Float)
    message = Column(Text)


    def __init__(self, id_user, id_chat, timestamp, message):
        self.id_user = id_user
        self.id_chat = id_chat
        self.time = timestamp
        self.message = message

    def __repr__(self):
        return "ChatMsg {} <{} to {}: {}>".format(
            self.id, self.id_user, self.id_chat,
            self.message[:10] + ("..." if len(message) > 10 else ""))


class Contact(Base):
    __tablename__ = "contacts"
    id = Column("id", Integer, primary_key=True)
    id_user = Column("id_user", String, ForeignKey("users.id"))
    id_contact = Column("id_contact", String, ForeignKey("users.id"))
    __uix = UniqueConstraint("id_user", "id_contact")


    def __init__(self, id_user, id_contact):
        self.id_user = id_user
        self.id_contact = id_contact

    def __repr__(self):
        return "UserContact {} : {}".format(self.id_user, self.id_contact)

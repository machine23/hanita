from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text
from sqlalchemy import UniqueConstraint, CheckConstraint
from JIM import JIMMessage

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    name = Column(String(25))
    status = Column(String(8), nullable=False)
    CheckConstraint("status in ('active', 'deleted')")

    def __init__(self, name):
        self.name = name
        self.status = "active"

    def __repr__(self):
        return "User (userid = {}, name = {})".format(
            self.id, self.name)



class Chat(Base):
    __tablename__ = "chats"
    id = Column("id", Integer, primary_key=True)
    name = Column(String(25))
    status = Column(String(8), nullable=False)
    CheckConstraint("status in ('active', 'deleted')")

    def __init__(self, name):
        self.name = name
        self.status = "active"

    def __repr__(self):
        return "Chat <{}, {}>".format(self.id, self.name)


class ChatUser(Base):
    __tablename__ = "chat_users"
    id = Column("id", Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(8), nullable=False)
    CheckConstraint("status in ('active', 'deleted')")
    __uix = UniqueConstraint(chat_id, user_id)

    def __init__(self, chat_id, user_id):
        self.chat_id = chat_id
        self.user_id = user_id
        self.status = "active"

    def __repr__(self):
        return "ChatUser {}".format(self.id)


class ChatMsg(Base):
    __tablename__ = "chat_msgs"
    id = Column("id", Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    chat_id = Column(Integer, ForeignKey("chats.id"))
    time = Column(Float)
    message = Column(Text)
    status = Column(String(8))
    CheckConstraint("status in ('active', 'deleted')")

    def __init__(self, msg: JIMMessage):
        if not msg.action == JIMMessage.MSG:
            raise 
        self.user_id = msg.from_user
        self.chat_id = msg.to_user
        self.time = msg.time
        self.message = msg.message
        self.status = "active"

    def __repr__(self):
        return "ChatMsg {} <{} to {}: {}>".format(
            self.id, self.user_id, self.chat_id,
            self.message[:10] + ("..." if len(self.message) > 10 else ""))


class Contact(Base):
    __tablename__ = "contacts"
    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", String, ForeignKey("users.id"))
    contact_id = Column("contact_id", String, ForeignKey("users.id"))
    status = Column(String(8), nullable=False)
    CheckConstraint("status in ('active', 'deleted')")
    __uix = UniqueConstraint("user_id", "contact_id")

    def __init__(self, user_id, contact_id):
        self.user_id = user_id
        self.contact_id = contact_id
        self.status = "active"

    def __repr__(self):
        return "UserContact {} : {}".format(self.user_id, self.contact_id)

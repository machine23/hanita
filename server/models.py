from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Float


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    # id = Column(Integer, primary_key=True)
    user_id = Column(String(25), primary_key=True)
    password = Column(String(25))

    def __init__(self, name, password=""):
        self.user_id = name
        self.password = password

    def __repr__(self):
        return "User (userid = {}, password = {})".format(self.user_id,
                                                          self.password)


class UserHistory(Base):
    __tablename__ = "user_hist"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    login_time = Column(Float)
    login_ip = Column(String(15))

    def __init__(self, user, login_time, login_ip):
        if not isinstance(user, User):
            raise
        self.user_id = user.user_id
        self.login_time = login_time
        self.login_ip = login_ip

    def __repr__(self):
        return "UserHistory {} ({}, {})".format(self.user_id, self.login_time,
                                                self.login_ip)


class UserContact(Base):
    __tablename__ = "user_cont"
    id = Column(Integer, primary_key=True)
    user_id = Column("user_id", String, ForeignKey("users.user_id"))
    contact_id = Column("contact_id", String, ForeignKey("users.user_id"))

    def __init__(self, user, contact):
        if not (isinstance(user, User) and isinstance(contact, User)):
            raise
        self.user_id = user.user_id
        self.contact_id = contact.user_id

    def __repr__(self):
        return "UserContact {} : {}".format(self.user_id, self.contact_id)

""" Модель данных для клиента """
import sqlite3
import threading

from JIM import JIMMessage, JIMClientMessage


class ClientDBError(Exception):
    pass


class ClientDB:
    def __init__(self, path_to_db=None):
        self._observers = []
        self._active_chat = None
        self._active_user = None
        self.lock = threading.Lock()
        if not path_to_db:
            path_to_db = ":memory:"
        self.conn = sqlite3.connect(path_to_db, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.setup()

    @property
    def active_user(self):
        return self._active_user

    @active_user.setter
    def active_user(self, user_name):
        self._active_user = user_name
        self.add_user(user_name)

    @property
    def active_chat(self):
        return self._active_chat

    @active_chat.setter
    def active_chat(self, chat_name):
        self._active_chat = chat_name
        self.add_chat(chat_name)

    def setup(self):
        """ Создаем таблицы """
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT UNIQUE
            );
            CREATE TABLE IF NOT EXISTS chats(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_name TEXT UNIQUE
            );
            CREATE TABLE IF NOT EXISTS chat_users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                chat_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (chat_id) REFERENCES chats(id),
                CONSTRAINT  unique_user_for_chat UNIQUE (user_id, chat_id)
            );
            CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator_id INTEGER,
                chat_id INTEGER,
                time REAL,
                message TEXT,
                FOREIGN KEY (creator_id) REFERENCES users(id),
                FOREIGN KEY (chat_id) REFERENCES chats(id)
            );
            """)
        self.conn.commit()

    def add_user(self, user_name):
        """ Добавить пользователя """
        if not self.user_exists(user_name):
            cmd = "INSERT INTO users(user_name) VALUES (?)"
            self.lock.acquire()
            self.cursor.execute(cmd, (user_name, ))
            self.conn.commit()
            self.lock.release()
        self._notify()

    def get_users(self):
        """ Получить список пользователей """
        self.lock.acquire()
        self.cursor.execute("SELECT * FROM users;")
        arr = self.cursor.fetchall()
        self.lock.release()
        users = [i[1] for i in arr]
        return users

    def get_user_id(self, user_name):
        """ Получить id пользователя """
        cmd = "SELECT users.id FROM users WHERE users.user_name = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (user_name, ))
        _id = self.cursor.fetchall()
        self.lock.release()
        return _id[0][0] if _id else None

    def get_user_name(self, user_id):
        """ Получить имя пользователя по id """
        cmd = "SELECT user_name FROM users WHERE users.id = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (user_id, ))
        res = self.cursor.fetchall()
        self.lock.release()
        return res[0][0] if res else None

    def user_exists(self, user_name):
        """ Проверить наличие пользователя """
        cmd = "SELECT 1 FROM users WHERE users.user_name = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (user_name, ))
        answer = bool(self.cursor.fetchall())
        self.lock.release()
        return answer

    def get_chats(self):
        """ получить список имеющихся чатов """
        cmd = "SELECT chats.chat_name FROM chats"
        self.lock.acquire()
        self.cursor.execute(cmd)
        arr = self.cursor.fetchall()
        self.lock.release()
        chats = [i[0] for i in arr]
        return chats

    def add_chat(self, chat_name):
        """ Добавить чат в бд """
        if not self.chat_exists(chat_name):
            cmd = "INSERT INTO chats(chat_name) VALUES (?)"
            self.lock.acquire()
            self.cursor.execute(cmd, (chat_name, ))
            self.conn.commit()
            self.lock.release()
        self._notify()

    def chat_exists(self, chat_name):
        """ проверить наличие чата в бд """
        cmd = "SELECT 1 FROM chats WHERE chats.chat_name = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (chat_name, ))
        answer = bool(self.cursor.fetchall())
        self.lock.release()
        return answer

    def get_chat_id(self, chat_name):
        """ получить id по имени чата """
        cmd = "SELECT id FROM chats WHERE chats.chat_name = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (chat_name, ))
        _id = self.cursor.fetchall()
        self.lock.release()
        return _id[0][0] if _id else None

    def get_chat_name(self, chat_id):
        """ получить имя чата по id """
        cmd = "SELECT chat_name FROM chats WHERE chats.id = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (chat_id, ))
        res = self.cursor.fetchall()
        self.lock.release()
        return res[0][0] if res else None

    def add_chat_user(self, user_name, chat_name):
        """ добавить пользователя в чат """
        if not (self.user_exists(user_name) and self.chat_exists(chat_name)):
            raise ClientDBError("add_chat_user error")
        cmd = "INSERT INTO chat_users(user_id, chat_id) VALUES (?, ?)"
        user_id = self.get_user_id(user_name)
        chat_id = self.get_chat_id(chat_name)
        try:
            self.lock.acquire()
            self.cursor.execute(cmd, (user_id, chat_id))
        except sqlite3.Error as err:
            raise ClientDBError(err)
        else:
            self.conn.commit()
        finally:
            self.lock.release()
        self._notify()

    def get_chat_users(self, chat_name):
        """ получить список пользователей чата """
        chat_id = self.get_chat_id(chat_name)
        cmd = "SELECT user_id FROM chat_users WHERE chat_users.chat_id = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (chat_id, ))
        res = self.cursor.fetchall()
        self.lock.release()
        users = [self.get_user_name(i[0]) for i in res if i]
        return users

    def add_message(self, message: JIMClientMessage):
        """ добавить сообщение в бд """
        if not (isinstance(message, JIMMessage) and message.action == "msg"):
            raise ClientDBError("message must be JIMClientMessage.msg")
        ### Временное упрощение ############################
        # Добавляем чат и пользователя из сообщения без проверки на сервере
        chat_name = message.to_user
        if not self.chat_exists(chat_name):
            self.add_chat(chat_name)
        user_name = message.from_user
        if not self.user_exists(user_name):
            self.add_user(user_name)
        try:
            self.add_chat_user(user_name, chat_name)
        except ClientDBError:
            pass
        ####################################################
        chat_id = self.get_chat_id(message.to_user)
        creator_id = self.get_user_id(message.from_user)
        # print(chat_id, creator_id)
        cmd = """INSERT INTO messages(creator_id, chat_id, time, message)
                 VALUES (?, ?, ?, ?)"""
        if chat_id and creator_id:
            self.lock.acquire()
            self.cursor.execute(
                cmd, (creator_id, chat_id, message.time, message.message))
            self.conn.commit()
            self.lock.release()
        else:
            raise ClientDBError("unknown creator or chat")
        self._notify()

    def get_messages(self, chat_name):
        cmd = """SELECT creator_id, chat_id, time, message
                 FROM messages
                 WHERE messages.chat_id = ?"""
        chat_id = self.get_chat_id(chat_name)
        self.lock.acquire()
        self.cursor.execute(cmd, (chat_id, ))
        data = self.cursor.fetchall()
        self.lock.release()
        messages = []
        for item in data:
            msg = JIMMessage()
            msg.from_user = self.get_user_name(item[0])
            msg.to_user = self.get_chat_name(item[1])
            msg.time = item[2]
            msg.message = item[3]
            msg.action = "msg"
            messages.append(msg)
        return messages

    def add_observer(self, observer):
        self._observers.append(observer)

    def del_observer(self, observer):
        self._observers.remove(observer)

    def _notify(self):
        # print("notified")
        for observer in self._observers:
            observer.model_is_changed()

    def close(self):
        """ Закрываем соединение с БД """
        if self.conn:
            self.conn.close()
            self.conn = None

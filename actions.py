import time


PRESENCE = "presence"
MSG = "msg"

actions_list = (PRESENCE, MSG)


class Actions:
    def __init__(self, user):
        self.user = user

    def create_presence(self, status=None, timestamp=None):
        """ Создает сообщение presence """
        if timestamp is None:
            timestamp = time.time()
        msg = {
            "action": PRESENCE,
            "time": timestamp,
            "type": "status",
            "user": {
                "account_name": self.user,
                "status": status
            }
        }
        return msg

    def create_msg(self, to_user, message, encoding="ascii", timestamp=None):
        """ 
        Создает простое сообщение msg.
        Если to_user имеет префикс #, то это сообщение для группы
        """
        if timestamp is None:
            timestamp = time.time()
        if message:
            msg = {
                "action": MSG,
                "time": timestamp,
                "to": to_user,
                "from": self.user,
                "encoding": encoding,
                "message": message
            }
            return msg

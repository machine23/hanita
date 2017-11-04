import time


PRESENCE = "presence"
MSG = "msg"

actions_list = (PRESENCE, MSG)


def create_presence(user, status=None, timestamp=None):
    """ Создает сообщение presence """
    if timestamp is None:
        timestamp = time.time()
    msg = {
        "action": PRESENCE,
        "time": timestamp,
        "type": "status",
        "user": {
            "account_name": user,
            "status": status
        }
    }
    return msg

def create_msg(user, to_user, message, encoding="ascii", timestamp=None):
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
            "from": user,
            "encoding": encoding,
            "message": message
        }
        return msg

import functools
import logging

import log_config


logger = logging.getLogger("server.main")


def log(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        msg = ", ".join(str(item) for item in args) if args else ""
        if kwargs:
            s_kwargs = ", ".join(
                "{}={}".format(k, v) for k, v in kwargs.items()
            )
            msg += (", " if msg else "") + s_kwargs
        name = func.__name__
        logger.info("%s (%s)", name, msg)
        return func(*args, **kwargs)
    return inner

import logging
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger("server.main")

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s\t%(module)s %(message)s")

file_handler = TimedRotatingFileHandler(
    "server.main.log",
    when="D",
    interval=1,
    backupCount=3
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

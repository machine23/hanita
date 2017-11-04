import logging


logger = logging.getLogger("server.main")

formatter = logging.Formatter(
    "$(asctime)s $(levelname)s $(module)s $(funcName)s $(message)s")

file_handler = logging.FileHandler("server.main.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

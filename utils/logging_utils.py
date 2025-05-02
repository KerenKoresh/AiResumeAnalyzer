import os

from logtail.handler import LogtailHandler

from src.logger import logger


def add_logtail_handler():
    logger.handlers = [h for h in logger.handlers if not isinstance(h, LogtailHandler)]
    source_token = os.getenv("SOURCE_TOKEN")
    host = os.getenv("HOST")
    handler = LogtailHandler(source_token=source_token, host=host)
    logger.addHandler(handler)
    logger.info("Logtail handler added")

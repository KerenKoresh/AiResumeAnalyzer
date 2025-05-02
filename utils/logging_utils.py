import logging
import requests


class LogtailHandler(logging.Handler):
    def __init__(self, source_token, host):
        super().__init__()
        self.source_token = source_token
        self.host = host
        self.url = f'https://{self.host}/v1/logs'

    def emit(self, record):
        log_entry = self.format(record)
        payload = {'source_token': self.source_token, 'log': log_entry}
        requests.post(self.url, json=payload)


# עכשיו תוכל להוסיף את ה-handler הזה
import os

from src.logger import logger


def add_logtail_handler():
    logger.handlers = [h for h in logger.handlers if not isinstance(h, LogtailHandler)]
    source_token = os.getenv("SOURCE_TOKEN")
    host = os.getenv("HOST")
    handler = LogtailHandler(source_token=source_token, host=host)
    logger.addHandler(handler)
    logger.info("Logtail handler added")

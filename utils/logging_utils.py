import os
import requests
import logging

from datetime import datetime

# הגדרת logger
logger = logging.getLogger('betterstack_logger')
logger.setLevel(logging.INFO)


class BetterStackHandler(logging.Handler):
    def __init__(self, source_token, host):
        super().__init__()
        self.source_token = source_token
        self.host = host
        self.url = f'{self.host}/api/logs'

    def emit(self, record):
        log_entry = self.format(record)
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        headers = {'Authorization': f'Bearer {self.source_token}', 'Content-Type': 'application/json'}
        payload = {
            "dt": timestamp,
            "message": log_entry
        }
        response = requests.post(self.url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"Error sending log: {response.text}")


def add_betterstack_handler():
    # הוספת ה-handler של BetterStack
    logger.handlers = [h for h in logger.handlers if not isinstance(h, BetterStackHandler)]

    source_token = os.getenv("SOURCE_TOKEN")
    host = os.getenv("HOST")

    handler = BetterStackHandler(source_token=source_token, host=host)
    logger.addHandler(handler)
    logger.info("BetterStack handler added")


# הוספת ה-handler עם הקריאה לפונקציה
add_betterstack_handler()

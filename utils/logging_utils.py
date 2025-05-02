import os
import requests
import logging

from datetime import datetime

# הגדרת logger
logger = logging.getLogger('betterstack_logger')
logger.setLevel(logging.INFO)


class BetterStackHandler:
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def emit(self, record):
        payload = {
            "dt": record.created,
            "message": record.msg,
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # אם ה-URL לא כולל סכימה, נוסיף אותה
        if not self.url.startswith(('http://', 'https://')):
            self.url = 'https://' + self.url

        try:
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()  # יזרוק חריגה אם הסטטוס לא 200
        except requests.exceptions.RequestException as e:
            print(f"Error sending log to BetterStack: {e}")

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

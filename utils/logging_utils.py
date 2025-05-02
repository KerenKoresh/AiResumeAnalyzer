import os
import logging
import requests


class BetterStackHandler(logging.Handler):
    def __init__(self, url, token):
        super().__init__()
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
    source_token = os.getenv("SOURCE_TOKEN")
    host = os.getenv("HOST")

    # ודא שהמשתנים קיימים
    if not source_token or not host:
        raise ValueError("SOURCE_TOKEN or HOST is not set in the environment variables.")

    handler = BetterStackHandler(url=host, token=source_token)

    # קבלת הלוגר מהמקום שבו הוא מוגדר
    logger = logging.getLogger('betterstack_logger')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.info("BetterStack handler added")

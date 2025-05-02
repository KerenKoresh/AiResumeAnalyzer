import logging
import requests
import streamlit as st

class BetterStackHandler(logging.Handler):

    def __init__(self, url, token):
        super().__init__()
        self.url = url
        self.token = token

    def emit(self, record):
        payload = {
            "dt": record.created,
            "message": record.getMessage(),
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error sending log to BetterStack: {e}")


def add_betterstack_handler():
    try:
        source_token = st.secrets["SOURCE_TOKEN"]
        host = st.secrets["HOST"]
    except Exception as e:
        raise ValueError("Missing SOURCE_TOKEN or HOST in Streamlit secrets.") from e

    logger = logging.getLogger('betterstack_logger')

    # בדיקה: אל תוסיף שוב אם כבר קיים
    if not any(isinstance(h, BetterStackHandler) for h in logger.handlers):
        handler = BetterStackHandler(url=host, token=source_token)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    logger.info("BetterStack handler added")

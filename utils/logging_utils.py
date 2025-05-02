# logging_utils.py
import logging
import requests
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # טוען משתני סביבה מקובץ .env (לשימוש מקומי)

class BetterStackHandler(logging.Handler):
    def __init__(self, source_token, host):
        super().__init__()
        self.source_token = source_token
        self.host = host

    def emit(self, record):
        log_entry = self.format(record)
        try:
            requests.post(
                self.host,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.source_token}",
                },
                json={"message": log_entry}
            )
        except Exception as e:
            logging.error(f"Failed to send log to BetterStack: {e}")


def get_secret(key):
    if key in st.secrets:
        return st.secrets[key]
    return os.getenv(key)


def add_betterstack_handler():
    logger = logging.getLogger("AIResumeAnalyzer")  # הגדרת ה-logger כאן כדי להיות ייחודי

    # בדיקה אם כבר קיים handler מסוג BetterStackHandler
    if any(isinstance(handler, BetterStackHandler) for handler in logger.handlers):
        logging.info("🔔 BetterStack handler already added.")
        return

    source_token = st.secrets.get("SOURCE_TOKEN")
    host = st.secrets.get("HOST")

    if not source_token or not host:
        raise ValueError("SOURCE_TOKEN or HOST is not set in secrets or environment variables.")

    if not host.startswith("http"):
        raise ValueError("HOST must include schema, e.g., https://in.logs.betterstack.com")

    logger.setLevel(logging.INFO)

    handler = BetterStackHandler(source_token, host)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logging.info(f"🔔 BetterStack handler added. Total handlers: {len(logger.handlers)}")

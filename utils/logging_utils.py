import logging
import streamlit as st
import requests
import os
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
            print(f"Failed to send log to BetterStack: {e}")


_logger_initialized = False


def get_secret(key):
    # קודם כל מנסה מה-secrets של Streamlit Cloud, אחרת מהסביבה המקומית
    if key in st.secrets:
        return st.secrets[key]
    return os.getenv(key)


def add_betterstack_handler():
    global _logger_initialized
    if _logger_initialized:
        return

    source_token = get_secret("SOURCE_TOKEN")
    host = get_secret("HOST")

    if not source_token or not host:
        raise ValueError("SOURCE_TOKEN or HOST is not set in secrets or environment variables.")

    if not host.startswith("http"):
        raise ValueError("HOST must include schema, e.g., https://in.logs.betterstack.com")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = BetterStackHandler(source_token, host)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info("✅ BetterStack handler added successfully")

    _logger_initialized = True

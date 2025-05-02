import logging
import requests
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # טוען משתני סביבה מקובץ .env (לשימוש מקומי)

# סימון שה-logger כבר הוגדר
logger_initialized = False

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
    global logger_initialized  # השתמש במשתנה גלובלי

    if logger_initialized:  # אם ה-logger כבר הוגדר
        logging.info("🔔 BetterStack handler already exists.")
        return

    logger = logging.getLogger("AIResumeAnalyzer")
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

    logger_initialized = True  # עדכון המצב שה-logger הוגדר
    logging.info(f"🔔 BetterStack handler added. Total handlers: {len(logger.handlers)}")


def init_logger():
    global logger_initialized  # השתמש במשתנה גלובלי

    # אם ה-logger לא הוגדר עדיין, הוסף את ה-stream handler
    if not logger_initialized:
        logger = logging.getLogger("AIResumeAnalyzer")

        # הוסף את ה-StreamHandler אם הוא לא קיים
        if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            logging.info("🔔 StreamHandler added.")
        else:
            logging.info("🔔 StreamHandler already exists.")

        # הוסף את ה-handler של BetterStack
        add_betterstack_handler()

    else:
        logging.info("🔔 Logger already initialized.")

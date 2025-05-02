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
    # קודם כל מנסה מה-secrets של Streamlit Cloud, אחרת מהסביבה המקומית
    if key in st.secrets:
        return st.secrets[key]
    return os.getenv(key)


def add_betterstack_handler():
    logger = logging.getLogger()

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


def init_logger():
    # אתחול של הלוגר אם הוא לא הותקן קודם
    if "logger_initialized" not in st.session_state:
        logging.info("🔔 Logging test: logger initialized")

        # בדיקה אם ה-handler של BetterStack כבר הוסף
        if not any(isinstance(handler, BetterStackHandler) for handler in logging.getLogger().handlers):
            add_betterstack_handler()  # הוסף את ה-handler רק אם הוא לא קיים
            logging.info("🔔 BetterStack handler added.")
            st.session_state.logger_initialized = True
        else:
            logging.info("🔔 BetterStack handler already exists.")

    else:
        logging.debug("🔔 Logger already initialized previously.")

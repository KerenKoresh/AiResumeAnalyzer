import logging
import requests
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # טוען משתני סביבה מקובץ .env

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
    logger = logging.getLogger("AIResumeAnalyzer")

    # אם כבר יש BetterStack handler, אל נוסיף אחד נוסף
    if any(isinstance(handler, BetterStackHandler) for handler in logger.handlers):
        logging.info("🔔 BetterStack handler already exists.")
        return

    source_token = st.secrets.get("SOURCE_TOKEN")
    host = st.secrets.get("HOST")

    if not source_token or not host:
        raise ValueError("SOURCE_TOKEN or HOST is not set in secrets or environment variables.")

    if not host.startswith("http"):
        raise ValueError("HOST must include schema, e.g., https://in.logs.betterstack.com")

    handler = BetterStackHandler(source_token, host)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logging.info(f"🔔 BetterStack handler added. Total handlers: {len(logger.handlers)}")


def init_logger():
    # אם session_state לא מאותחל, אתחיל אותו
    if "logger_initialized" not in st.session_state:
        st.session_state["logger_initialized"] = False

    # אם הלוגר כבר מאותחל, אין צורך לאתחל אותו שוב
    if st.session_state["logger_initialized"]:
        logging.info("🔔 Logger is already initialized.")
        return

    # אתחול של הלוגר
    logger = logging.getLogger("AIResumeAnalyzer")

    # הוסף את ה-StreamHandler רק אם הוא לא קיים כבר
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logging.info("🔔 StreamHandler added.")

    # הוסף את ה-handler של BetterStack אם הוא לא קיים כבר
    add_betterstack_handler()

    # סמן שהלוגר מאותחל
    st.session_state["logger_initialized"] = True
    logging.info("🔔 Logger initialized successfully.")


# קריאה ל-init_logger() תתבצע אחרי האתחול של session_state
init_logger()

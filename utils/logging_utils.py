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
            # הימנע מלוג נוסף כאן כדי לא ליצור לולאת שגיאות
            print(f"[BetterStackHandler] Failed to send log: {e}")


def get_secret(key):
    if key in st.secrets:
        return st.secrets[key]
    return os.getenv(key)


def add_betterstack_handler():
    logger = logging.getLogger("AIResumeAnalyzer")

    if any(isinstance(handler, BetterStackHandler) for handler in logger.handlers):
        logger.info("🔔 BetterStack handler already exists.")
        return

    source_token = get_secret("SOURCE_TOKEN")
    host = get_secret("HOST")

    if not source_token or not host:
        raise ValueError("SOURCE_TOKEN or HOST is not set in secrets or environment variables.")

    if not host.startswith("http"):
        raise ValueError("HOST must include schema, e.g., https://in.logs.betterstack.com")

    handler = BetterStackHandler(source_token, host)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info(f"🔔 BetterStack handler added. Total handlers: {len(logger.handlers)}")


def init_logger():
    logger = logging.getLogger("AIResumeAnalyzer")
    logger.setLevel(logging.INFO)  # חשוב כדי לוודא שכל הלוגים יעברו

    if "logger_initialized" not in st.session_state:
        st.session_state["logger_initialized"] = False

    if st.session_state["logger_initialized"]:
        logger.info("🔔 Logger is already initialized.")
        return

    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info("🔔 StreamHandler added.")

    add_betterstack_handler()

    st.session_state["logger_initialized"] = True
    logger.info("🔔 Logger initialized successfully.")

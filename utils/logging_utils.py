import logging
import streamlit as st
import requests


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


def add_betterstack_handler():
    global _logger_initialized  # יש להגדיר את המשתנה כגלובלי
    if _logger_initialized:
        return  # כבר אותחל

    # שימוש נכון ב- st.secrets (גישה כמו מילון)
    source_token = st.secrets["SOURCE_TOKEN"]
    host = st.secrets["HOST"]

    if not source_token or not host:
        raise ValueError("SOURCE_TOKEN or HOST is not set in the environment variables.")

    if not host.startswith("http"):
        raise ValueError("HOST must include schema, e.g., https://in.logs.betterstack.com")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.info(f"Handlers count before: {len(logger.handlers)}")

    handler = BetterStackHandler(source_token, host)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info("BetterStack handler added")
    logger.info(f"Handlers count after: {len(logger.handlers)}")

    _logger_initialized = True  # עדכון המשתנה הגלובלי

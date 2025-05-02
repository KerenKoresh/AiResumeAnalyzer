import logging
import os

from dotenv import load_dotenv
import streamlit as st
from logtail.handler import LogtailHandler

load_dotenv()  # טוען את המשתנים מקובץ .env

source_token = os.getenv("SOURCE_TOKEN")
host = os.getenv("HOST")

logger = logging.getLogger("ai_resume_analyzer")
logger.setLevel(logging.INFO)

if 'logger_initialized' not in st.session_state:
    if not any(isinstance(h, LogtailHandler) for h in logger.handlers):
        handler = LogtailHandler(source_token=source_token, host=host)
        logger.addHandler(handler)
        logger.info("Logtail handler added")
    else:
        logger.info("Logtail handler already exists")

    st.session_state['logger_initialized'] = True

if 'log_message_logged' not in st.session_state:
    logger.info("This is a log message.")
    st.session_state['log_message_logged'] = True  # נסמן שהלוג בוצע


import logging
import os
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

def add_betterstack_handler():
    source_token = os.getenv("SOURCE_TOKEN")
    host = os.getenv("HOST")

    if not source_token or not host:
        raise ValueError("SOURCE_TOKEN or HOST is not set in the environment variables.")

    if not host.startswith("http"):
        raise ValueError("HOST must include schema, e.g., https://in.logs.betterstack.com")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # לוג של מספר ה-handlers הנוכחיים
    logger.info(f"Handlers count: {len(logger.handlers)}")

    if not any(isinstance(h, BetterStackHandler) for h in logger.handlers):
        handler = BetterStackHandler(source_token, host)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info("BetterStack handler added")

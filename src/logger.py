import logging
from utils.logging_utils import add_betterstack_handler

# Create a named logger
logger = logging.getLogger("AIResumeAnalyzer")


def init_logger():
    """
    Initialize the logger by adding the BetterStack handler if not already added.
    Should be called once at the start of the app.
    """
    add_betterstack_handler(logger)
    logger.info("Logger initialized and BetterStack handler added.")

# logger.py
import logging
from utils.logging_utils import add_betterstack_handler

logger = logging.getLogger("AIResumeAnalyzer")

# הוספת ה-handler של BetterStack
add_betterstack_handler(logger)

# דוגמה לשימוש בלוגר
logger.info("Logger initialized and BetterStack handler added.")

# בדוק את כל ה-handlers שהוספו
for handler in logger.handlers:
    print(f"Handler added: {handler}")

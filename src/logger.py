import logging
from utils.logging_utils import add_betterstack_handler

# קביעת level של הלוגר
logger = logging.getLogger('betterstack_logger')
logger.setLevel(logging.INFO)

# הוספת ה-handler של BetterStack
add_betterstack_handler()

# דוגמה לשימוש בלוגר
logger.info("Logger initialized and BetterStack handler added.")

# בדוק את כל ה-handlers שהוספו
for handler in logger.handlers:
    print(f"Handler added: {handler}")

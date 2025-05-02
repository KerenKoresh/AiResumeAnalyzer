import logging
from utils.logging_utils import add_betterstack_handler

# קביעת level של הלוגר
logger = logging.getLogger('betterstack_logger')
logger.setLevel(logging.INFO)

# הוספת ה-handler של BetterStack
add_betterstack_handler()

# דוגמה לשימוש בלוגר
logger.info("Logger initialized and BetterStack handler added.")

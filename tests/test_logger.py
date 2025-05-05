# tests/test_logger_integration.py

import unittest
import logging
from utils.logging_utils import add_betterstack_handler, BetterStackHandler


class TestLoggerIntegration(unittest.TestCase):
    def test_betterstack_handler_is_added(self):
        logger = logging.getLogger("AIResumeAnalyzer")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()

        add_betterstack_handler(logger)

        has_betterstack = any(isinstance(h, BetterStackHandler) for h in logger.handlers)
        self.assertTrue(has_betterstack, "BetterStackHandler was not added to logger.")

    def test_log_message_is_handled(self):
        logger = logging.getLogger("AIResumeAnalyzer")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()

        add_betterstack_handler(logger)

        with self.assertLogs(logger, level="INFO") as log:
            logger.info("🔍 Test log message to BetterStack")

        self.assertIn("🔍 Test log message to BetterStack", log.output[0])

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch
import logging
from utils.logging_utils import add_betterstack_handler, get_secret, BetterStackHandler

class TestLoggingUtils(unittest.TestCase):

    @patch("utils.logging_utils.st")
    def test_add_betterstack_handler_already_exists(self, mock_st):
        # Mock the necessary secrets
        mock_st.secrets = {
            "SOURCE_TOKEN": "dummy_token",
            "HOST": "https://dummyhost.com"
        }

        # Create a logger with a pre-existing BetterStackHandler
        test_logger = logging.getLogger("AIResumeAnalyzer")
        test_logger.handlers.clear()  # Clear any existing handlers
        test_logger.addHandler(BetterStackHandler("dummy_token", "https://dummyhost.com"))

        # Call the function to add the BetterStackHandler again
        add_betterstack_handler(test_logger)

        # Ensure the handler is not added again
        self.assertEqual(len(test_logger.handlers), 1)

    @patch("utils.logging_utils.st")
    def test_add_betterstack_handler_missing_secrets(self, mock_st):
        # Simulate missing secrets
        mock_st.secrets = {}

        # Create a logger for testing
        test_logger = logging.getLogger("AIResumeAnalyzer")
        test_logger.handlers.clear()

        with self.assertRaises(ValueError):
            add_betterstack_handler(test_logger)

    @patch("utils.logging_utils.st")
    @patch("utils.logging_utils.os.getenv")
    def test_get_secret_from_secrets(self, mock_getenv, mock_st):
        mock_st.secrets = {
            "MY_SECRET": "secret_value"
        }
        result = get_secret("MY_SECRET")
        self.assertEqual(result, "secret_value")

    @patch("utils.logging_utils.st")
    @patch("utils.logging_utils.os.getenv")
    def test_get_secret_from_env(self, mock_getenv, mock_st):
        mock_st.secrets = {}
        mock_getenv.return_value = "env_secret_value"
        result = get_secret("MY_SECRET")
        self.assertEqual(result, "env_secret_value")


if __name__ == "__main__":
    unittest.main()

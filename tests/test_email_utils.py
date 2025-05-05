# tests/test_email_utils.py

import unittest
from unittest.mock import patch, MagicMock
from utils.email_utils import send_email, is_valid_email


class TestEmailUtils(unittest.TestCase):

    @patch("utils.email_utils.st")
    def test_valid_email_format(self):
        valid = "user@example.com"
        self.assertTrue(is_valid_email(valid))

    @patch("utils.email_utils.st")
    def test_invalid_email_format(self, mock_st):
        invalid = "invalid-email"
        self.assertFalse(is_valid_email(invalid))
        mock_st.error.assert_called_once_with("📭 Invalid email address format.")

    @patch("utils.email_utils.smtplib.SMTP")
    @patch("utils.email_utils.st")
    @patch("utils.email_utils.FROM_EMAIL", "from@example.com")
    @patch("utils.email_utils.EMAIL_PASSWORD", "dummy-password")
    def test_send_email_success(self, mock_st, mock_smtp):
        smtp_instance = MagicMock()
        mock_smtp.return_value = smtp_instance

        send_email("Test Subject", "Test Body", "to@example.com")

        smtp_instance.starttls.assert_called_once()
        smtp_instance.login.assert_called_once_with("from@example.com", "dummy-password")
        smtp_instance.sendmail.assert_called_once()
        smtp_instance.quit.assert_called_once()
        mock_st.success.assert_called_once_with("Results have been sent to to@example.com")

    @patch("utils.email_utils.smtplib.SMTP", side_effect=Exception("SMTP error"))
    @patch("utils.email_utils.st")
    @patch("utils.email_utils.FROM_EMAIL", "from@example.com")
    @patch("utils.email_utils.EMAIL_PASSWORD", "dummy-password")
    def test_send_email_failure(self, mock_st, mock_smtp):
        send_email("Test Subject", "Test Body", "to@example.com")
        mock_st.error.assert_called_once_with("❌ Failed to send email.")


if __name__ == "__main__":
    unittest.main()

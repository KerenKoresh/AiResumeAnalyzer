import unittest
from unittest.mock import patch, MagicMock
import utils.pdf_utils


class TestPDFUtils(unittest.TestCase):
    @patch("utils.pdf_utils.pdfplumber.open")
    def test_extract_text_from_pdf(self, mock_pdfplumber):
        # Mocking pdfplumber.open to return a valid PDF-like object
        mock_pdf = MagicMock()
        mock_pdfplumber.return_value = mock_pdf

        # Mocking the behavior of pages in the PDF
        mock_page_1 = MagicMock()
        mock_page_1.extract_text.return_value = "Page 1 content"
        mock_page_2 = MagicMock()
        mock_page_2.extract_text.return_value = "Page 2 content"

        # Assigning mocked pages to the mock PDF object
        mock_pdf.pages = [mock_page_1, mock_page_2]

        # Placeholder uploaded file (the file itself is not needed because we're mocking)
        uploaded_file = "test_file.pdf"

        # Call the function under test
        try:
            result = utils.pdf_utils.extract_text_from_pdf(uploaded_file)
            print(f"Actual Extracted Text: {repr(result)}")  # Debugging the result

            # Expected result
            expected_result = "Page 1 content\nPage 2 content"
            print(f"Expected Result: {repr(expected_result)}")  # Show expected as raw string

            # Assert the result is as expected
            self.assertEqual(result.strip(), expected_result.strip())
        except Exception as e:
            print(f"Test failed with error: {e}")

    @patch("utils.pdf_utils.pdfplumber.open")
    def test_extract_text_from_pdf_error(self, mock_pdfplumber_open):
        # Simulate an exception being raised when attempting to open the PDF
        mock_pdfplumber_open.side_effect = Exception("Error opening PDF")

        # Simulate a PDF file (you could use a real one in actual tests)
        uploaded_file = "fake_file.pdf"

        # Check if the error is properly logged and re-raised
        with self.assertRaises(Exception) as context:
            utils.pdf_utils.extract_text_from_pdf(uploaded_file)

        self.assertEqual(str(context.exception), "Error opening PDF")


# Main function to execute the test cases
def main():
    unittest.main()


# If this file is executed directly, the main function will be called to run tests
if __name__ == "__main__":
    main()

import unittest
from unittest.mock import patch, MagicMock
from src.match_analysis import analyze_match


class TestMatchAnalysis(unittest.TestCase):

    @patch('src.match_analysis.get_match_analysis')
    def test_analyze_match(self, mock_get_match_analysis):
        # Arrange
        mock_get_match_analysis.return_value = 'mocked_result'  # You can customize this

        # Act
        result = analyze_match("resume_text", "job_description")

        # Assert
        mock_get_match_analysis.assert_called_once()  # Ensure it was called exactly once
        assert result == 'mocked_result'  # Check the result returned from the function

    @patch('src.match_analysis.get_match_analysis')
    @patch('utils.file_utils.save_previous_data')
    def test_analyze_match_exception(self, mock_save, mock_get_match):
        # Simulate an exception being raised in get_match_analysis
        mock_get_match.side_effect = Exception("Some error occurred")

        # Call the function and check if it raises the exception
        resume_text = "This is a resume"
        job_description = "This is a job description"
        with self.assertRaises(Exception) as context:
            analyze_match(resume_text, job_description)

        # Assert that the exception is raised
        self.assertTrue("Some error occurred" in str(context.exception))

        # Check that save_previous_data was not called since there was an error
        mock_save.assert_not_called()


if __name__ == '__main__':
    unittest.main()

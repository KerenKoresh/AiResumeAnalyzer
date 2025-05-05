import unittest
from unittest.mock import patch
import utils.openai_utils


# This test class contains unit tests for the `get_match_analysis` function in `openai_utils.py`.
class TestOpenAIUtils(unittest.TestCase):

    # Test case for a valid response from the OpenAI API
    @patch("utils.openai_utils.openai.ChatCompletion.create")
    def test_get_match_analysis(self, mock_openai_create):
        # Mocking a valid response from OpenAI
        mock_openai_create.return_value = {
            "choices": [
                {"message": {"content": "Matched! Good fit for the job."}}
            ]
        }

        resume_text = "Experienced software engineer with skills in Python, JavaScript."
        job_description = "Looking for a software engineer with experience in Python and cloud technologies."

        # Call the function under test
        result = utils.openai_utils.get_match_analysis(resume_text, job_description)

        # Assert that the result matches the expected output
        self.assertEqual(result, "Matched! Good fit for the job.")

    # Test case for an empty response (no 'choices' key in the response)
    @patch("utils.openai_utils.openai.ChatCompletion.create")
    def test_get_match_analysis_empty_response(self, mock_openai_create):
        # Mocking an empty response to simulate an invalid API response
        mock_openai_create.return_value = {}

        resume_text = "Experienced software engineer with skills in Python, JavaScript."
        job_description = "Looking for a software engineer with experience in Python and cloud technologies."

        # Expecting a KeyError to be raised when the response doesn't contain the 'choices' key
        with self.assertRaises(KeyError):
            utils.openai_utils.get_match_analysis(resume_text, job_description)

    # Test case for an invalid response structure (incorrect key)
    @patch("utils.openai_utils.openai.ChatCompletion.create")
    def test_get_match_analysis_invalid_response(self, mock_openai_create):
        # Mocking an invalid response structure
        mock_openai_create.return_value = {
            "invalid_key": "some_value"
        }

        resume_text = "Experienced software engineer with skills in Python, JavaScript."
        job_description = "Looking for a software engineer with experience in Python and cloud technologies."

        # Expecting a KeyError to be raised when the response structure is invalid
        with self.assertRaises(KeyError):
            utils.openai_utils.get_match_analysis(resume_text, job_description)


# Main function to execute the test cases
def main():
    unittest.main()


# If this file is executed directly, the main function will be called to run tests
if __name__ == "__main__":
    main()

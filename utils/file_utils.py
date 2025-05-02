import json
import os


def read_previous_data(file_path='previous_data.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return None


def save_previous_data(resume_text, job_description, file_path='previous_data.json'):
    with open(file_path, 'w') as file:
        json.dump({
            'resume_text': resume_text,
            'job_description': job_description
        }, file)

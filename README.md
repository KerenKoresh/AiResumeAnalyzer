AiResumeAnalyzer
AiResumeAnalyzer is an AI-powered resume analysis tool that helps job seekers improve their resumes by providing personalized feedback. This project uses OpenAI's GPT to analyze resumes and offer suggestions for improvement based on job descriptions or best practices.

🚀 Features
📄 Upload resumes (PDF or text)

🔍 Analyze strengths, weaknesses, and skills

🎯 Tailor resume to a specific job description

📊 Get insights into how well your resume matches the desired role

🧠 Powered by GPT-4 for accurate, detailed feedback

🖥️ Web-based interface built with Streamlit

🛠️ Tech Stack
Python

Streamlit – UI

OpenAI API – Resume analysis

PyMuPDF / PDFParser – PDF parsing

dotenv – Manage environment variables like OpenAI API keys

💡 How It Works
Upload your resume.

(Optional) Provide a job description.

The AI will:

Parse the resume content.

Compare it with the job description.

Generate a detailed feedback report with suggestions for improvement.

Results are displayed in the Streamlit interface.

📦 Installation
bash
Copy
Edit
git clone https://github.com/KerenKoresh/AiResumeAnalyzer.git
cd AiResumeAnalyzer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
🔑 Environment Variables
Create a .env file in the root directory and add your OpenAI API key:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_api_key_here
▶️ Run the App
bash
Copy
Edit
streamlit run app.py
The app will open in your browser at http://localhost:8501.

📎 Example Use Case
Upload your resume and paste a job description like:

"Looking for a Senior Python Developer with experience in cloud platforms, CI/CD, and REST APIs."

The app will analyze how well your resume fits the role and suggest improvements such as:

Add more emphasis on REST API experience.

Mention tools like Docker or AWS.

🧩 To-Do / Roadmap
 User authentication

 Save analysis history

 Export feedback to PDF

 Integrate with LinkedIn profile importer

 Add multilingual support (Hebrew, etc.)

🤝 Contributing
Pull requests are welcome! If you'd like to contribute:

Fork the repo

Create a feature branch

Submit a PR

📄 License
MIT License. See LICENSE for more information.

✨ Acknowledgements
OpenAI

Streamlit

Inspiration from resume reviewers and career coaches


# AiResumeAnalyzer

**AiResumeAnalyzer** is an AI-powered resume analysis tool that helps job seekers optimize their resumes by providing personalized feedback. The project utilizes OpenAI's GPT to analyze resumes and provide improvement suggestions based on job descriptions or best practices.

![Logo](assets/logo.png)  <!-- Add an image or logo here -->

## 🚀 Features

- 📄 **Upload Resumes**: Upload resumes in PDF or text format.
- 🔍 **Analyze Strengths & Weaknesses**: Get feedback on key areas of improvement.
- 🎯 **Tailor Resume**: Align your resume with specific job descriptions.
- 📊 **Insightful Feedback**: Detailed suggestions to make your resume stand out.
- 🧠 **AI-powered**: Built on GPT-4 for accurate and contextual recommendations.
- 🖥️ **Web-based Interface**: User-friendly experience powered by [Streamlit](https://streamlit.io).

## 🛠️ Tech Stack

- `Python`
- `Streamlit` – Frontend UI
- `OpenAI API` – GPT for Resume Analysis
- `PyMuPDF` / `PDFParser` – Resume parsing from PDFs
- `dotenv` – For managing secrets like API keys

## 💡 How It Works

1. **Upload Your Resume**: Upload your resume in PDF or text format.
2. **(Optional) Provide a Job Description**: Add the job description to tailor your feedback.
3. **AI Analyzes the Resume**: The AI compares your resume with the job description and provides detailed feedback.
4. **Receive Feedback**: View AI-generated insights that can help improve your resume.

## 📦 Installation

To run the app locally, follow these steps:

```bash
git clone https://github.com/KerenKoresh/AiResumeAnalyzer.git
cd AiResumeAnalyzer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 🔑 Set Up Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## ▶️ Run the App

Run the following command to start the app:

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501` in your browser.

## 📎 Example Use Case

1. Upload your resume.
2. Paste a job description like this:

   > "Looking for a Senior Python Developer with experience in cloud platforms, CI/CD, and REST APIs."

3. **Get Detailed Feedback**: The app will analyze how well your resume fits the job and suggest areas of improvement.

## 🧩 Roadmap

Future features we are working on:

- [ ] User authentication
- [ ] Save analysis history
- [ ] Export feedback to PDF
- [ ] Integrate with LinkedIn profile importer
- [ ] Add multilingual support (Hebrew, etc.)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repo
2. Create a new branch
3. Submit a Pull Request

## 📄 License

MIT License. See `LICENSE` for more information.

## ✨ Acknowledgements

- [OpenAI](https://openai.com/) – For providing the powerful GPT-4 API.
- [Streamlit](https://streamlit.io) – For the easy-to-use interface framework.
- Inspiration from career coaches and resume reviewers.

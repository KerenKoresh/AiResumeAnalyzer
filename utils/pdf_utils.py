import pdfplumber
import logging

logger = logging.getLogger("AIResumeAnalyzer")

def extract_text_from_pdf(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            resume_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        logging.info("🔔 Text extracted from PDF successfully.")
        return resume_text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise e

import streamlit as st
from utils.analysis_utils import analyze_resume


def run():
    st.title("Analyze Resume")

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
    job_description = st.text_area("Enter the job description")
    email_address = st.text_input("Enter your email (optional)")

    if st.button("Analyze"):
        if uploaded_file and job_description:
            result = analyze_resume(uploaded_file, job_description, email_address)
            st.write(result)
        else:
            st.error("Please upload both a resume and a job description.")

import streamlit as st

def run():
    # הצגת הבר העליון עם הלוגו ושם האפליקציה
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; background-color: #f1f1f1;">
            <img src="https://yourlogo.com/logo.png" alt="Logo" width="50">
            <h1 style="margin: 0;">AI Resume Analyzer</h1>
        </div>
    """, unsafe_allow_html=True)

    st.title("Welcome to the Home Page")
    st.write("This is where you can get started with analyzing resumes.")

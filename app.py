# app.py
import streamlit as st
from pages import home, analyze  # או מהשם של התיקייה החדשה שתקרא לה "modules" למשל

PAGES = {
    "home": home,
    "analyze": analyze,
}

def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

    query_params = st.query_params
    page = query_params.get("page", "home").lower()

    with st.sidebar:
        st.markdown("## 📂 ניווט")
        st.markdown(f"""
            <a href='?page=home' style='text-decoration: none;'>🏠 דף הבית</a><br>
            <a href='?page=analyze' style='text-decoration: none;'>📄 ניתוח קורות חיים</a>
        """, unsafe_allow_html=True)

    if page in PAGES:
        PAGES[page].run()
    else:
        st.error("⚠️ העמוד לא נמצא.")

if __name__ == "__main__":
    main()

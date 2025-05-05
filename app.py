
import streamlit as st
from pages import home, login, register, analyze, settings


# הגדרת תפריט ניווט
def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

    # תפריט ניווט בין הדפים
    pages = {
        "Home": home,
        "Login": login,
        "Register": register,
        "Analyze": analyze,
        "Settings": settings,
    }

    # הצגת הבחירה של המשתמש בתפריט
    page = st.sidebar.selectbox("Choose a page", list(pages.keys()))

    # קריאה לדף המתאים לפי הבחירה
    pages[page].run()


if __name__ == "__main__":
    main()

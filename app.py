import streamlit as st
from pages import home, analyze

PAGES = {
    "home": home,
    "analyze": analyze,
}

def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

    # קריאת הפרמטרים מה-URL
    query_params = st.query_params
    page = query_params.get("page", "home").lower()

    # תפריט ניווט בצד
    with st.sidebar:
        st.markdown("## 📂 Menu")
        st.page_link("app.py", label="🏠 Home", params={"page": "home"})
        st.page_link("app.py", label="📄 Analyze Resume", params={"page": "analyze"})

    if page not in PAGES:
        st.error("Page not found.")
        return

    # הצגת הדף הרלוונטי
    PAGES[page].run()

if __name__ == "__main__":
    main()

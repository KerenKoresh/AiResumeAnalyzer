import streamlit as st
from pages import home, analyze

# הגדרת הדפים
PAGES = {
    "home": home,
    "analyze": analyze,
}

def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

    # קריאה מה-URL
    page = st.query_params.get("page", "home").lower()

    # Sidebar custom navigation
    with st.sidebar:
        st.markdown("## 📂 Navigation")
        # רק הוספתי את האפשרויות המתאימות (לא app, analyze, home או init)
        st.markdown(f"""
            <a href='?page=home' style='text-decoration: none; font-size: 16px;'>
                🏠 Home
            </a><br>
            <a href='?page=analyze' style='text-decoration: none; font-size: 16px;'>
                📄 Analyze Resume
            </a>
        """, unsafe_allow_html=True)

    # Load page based on URL parameter
    if page in PAGES:
        PAGES[page].run()
    else:
        st.error("Page not found.")

if __name__ == "__main__":
    main()

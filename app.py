import streamlit as st
from pages import home, analyze

# הגדרת הדפים שברצונך להציג
PAGES = {
    "home": home,
    "analyze": analyze,
}

def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

    # הצגת בר עליון עם הלוגו ושם האפליקציה
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; background-color: #f1f1f1;">
            <img src="https://yourlogo.com/logo.png" alt="Logo" width="50">
            <h1 style="margin: 0;">AI Resume Analyzer</h1>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar custom navigation
    with st.sidebar:
        st.markdown("## 📂 Navigation")
        # שמות הדפים הרצויים בלבד
        st.markdown(f"""
            <a href='?page=home' style='text-decoration: none; font-size: 16px;'>
                🏠 Home
            </a><br>
            <a href='?page=analyze' style='text-decoration: none; font-size: 16px;'>
                📄 Analyze Resume
            </a>
        """, unsafe_allow_html=True)

    # קריאה מה-URL (שימוש ב-experimental_get_query_params)
    page = st.experimental_get_query_params().get("page", ["home"])[0].lower()

    # טוען את הדף המתאים לפי ה-URL
    if page in PAGES:
        PAGES[page].run()
    else:
        st.error("Page not found.")

if __name__ == "__main__":
    main()

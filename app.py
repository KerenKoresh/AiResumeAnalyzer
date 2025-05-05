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

    # Sidebar custom navigation - כאן אנחנו רק מציגים את הדפים הביתיים
    with st.sidebar:
        st.markdown("## 📂 Navigation")
        # תצוגת ניווט בעזרת st.radio
        page = st.radio(
            "Choose a page:",
            options=["Home", "Analyze Resume"]
        )

    # טעינת הדף המתאים לפי הבחירה
    if page == "Home":
        PAGES["home"].run()
    elif page == "Analyze Resume":
        PAGES["analyze"].run()

if __name__ == "__main__":
    main()

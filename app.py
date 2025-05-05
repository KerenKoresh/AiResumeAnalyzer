import streamlit as st
from pages import home, analyze

PAGES = {
    "Home": home,
    "Analyze Resume": analyze,
}

def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

    # 🧼 הסתרת תפריט הניווט האוטומטי של Streamlit
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # 🔝 בר עליון עם לוגו ושם האפליקציה
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; padding: 10px 0;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/AI_Logo.png" width="40">
            <h2 style="margin: 0;">AI Resume Analyzer</h2>
        </div>
    """, unsafe_allow_html=True)

    # 📂 תפריט צד מותאם
    with st.sidebar:
        st.markdown("## 📂 Navigation")
        page = st.radio(
            "",  # בלי כותרת מעל
            list(PAGES.keys()),
            index=0,
        )

    # טעינת הדף המתאים
    PAGES[page].run()

if __name__ == "__main__":
    main()

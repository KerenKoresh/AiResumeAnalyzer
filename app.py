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
        <div style="display: flex; align-items: center; gap: 15px; padding: 10px 0 20px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/AI_Logo.png" width="36" height="36" style="border-radius: 5px;">
            <h1 style="margin: 0; font-size: 24px;">AI Resume Analyzer</h1>
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

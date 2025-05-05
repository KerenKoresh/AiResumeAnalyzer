import streamlit as st
import base64
from pages import home, analyze

PAGES = {
    "Home": home,
    "Analyze Resume": analyze,
}

# פונקציה שממירה לוגו ל-base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{encoded}"

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

    # 🔝 בר עליון עם לוגו מוגדל ושם האפליקציה
    logo_base64 = get_base64_image("assets/logo.png")  # ודאי שהנתיב נכון
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 20px; padding: 10px 0 30px;">
            <img src="{logo_base64}" width="64" height="64" style="border-radius: 10px;">
            <h1 style="margin: 0; font-size: 32px;">AI Resume Analyzer</h1>
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

import streamlit as st

def run():
    st.title("Settings")
    st.write("This is the settings page where you can adjust preferences or log out.")
    if st.button("Log out"):
        st.session_state["logged_in"] = False
        st.session_state["email"] = None
        st.success("You have been logged out.")

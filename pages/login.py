import streamlit as st
from utils.auth_utils import login_user


def run():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if login_user(email, password):
            st.session_state["logged_in"] = True
            st.session_state["email"] = email
            st.success("Successfully logged in.")
        else:
            st.error("Invalid email or password.")

import streamlit as st
from utils.auth_utils import register_user

def run():
    st.title("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if register_user(email, password):
            st.session_state["logged_in"] = True
            st.session_state["email"] = email
            st.success("Registration successful! You are now logged in.")
        else:
            st.error("Email already exists. Please try another email.")

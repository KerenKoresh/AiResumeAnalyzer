# pages/login.py

import streamlit as st
from utils.auth_utils import login_user, register_user, create_users_table

def run():
    # Create the users table if it doesn't exist
    create_users_table()

    st.title("🔒 Login / Register")

    # Login form
    login_form = st.form("login_form")
    with login_form:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Log In")

    # Registration form
    register_form = st.form("register_form")
    with register_form:
        register_email = st.text_input("Email", key="register_email")
        register_password = st.text_input("Password", type="password", key="register_password")
        register_button = st.form_submit_button("Register")

    # Handle login
    if login_button:
        if login_user(email, password):
            st.session_state["logged_in"] = True
            st.session_state["email"] = email
            st.success("Successfully logged in!")
            st.experimental_set_query_params(page="main")
            st.rerun()
        else:
            st.error("Invalid email or password.")

    # Handle registration
    if register_button:
        if register_email and register_password:
            register_user(register_email, register_password)
            st.success("Registration successful! You are now logged in.")
            st.session_state["logged_in"] = True
            st.session_state["email"] = register_email
            st.experimental_set_query_params(page="main")
            st.rerun()
        else:
            st.error("Please provide both email and password for registration.")

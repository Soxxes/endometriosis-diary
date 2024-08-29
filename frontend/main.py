import streamlit as st
from datetime import datetime
from helpers.auth import authenticate_user, register_user
from helpers.validate import (
    validate_birthday, validate_email, validate_height,
    validate_password, validate_username, validate_weight
)


def toggle_mode():
    st.session_state['login_mode'] = not st.session_state['login_mode']


if 'login_mode' not in st.session_state:
    st.session_state['login_mode'] = True

if st.session_state['login_mode']:
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state['authenticated'] = True
            st.success(f"Willkommen {username}!")
        else:
            st.session_state['authenticated'] = False
            st.error("Ungültige Benutzerdaten")
    
    st.button("Registrieren", on_click=toggle_mode)

else:
    st.title("Registrierung")

    username = st.text_input("Benutzername")
    email = st.text_input("Email")
    password = st.text_input("Passwort", type="password")
    height = st.number_input("Größe (m)", min_value=0.0)
    weight = st.number_input("Gewicht (kg)", min_value=0.0)
    birthday = st.date_input("Geburtsdatum",
                             min_value=datetime.strptime("01.01.1930", "%d.%m.%Y"),
                             max_value=datetime.strptime("01.01.2024", "%d.%m.%Y"),
                             format="DD.MM.YYYY").strftime("%Y-%m-%d")

    if st.button("Bestätigen"):
        valid = (
            validate_username(username) and
            validate_email(email) and
            validate_password(password) and
            validate_height(height) and
            validate_weight(weight) and
            validate_birthday(birthday)
        )
        if valid:
            success, err = register_user(username, email, password, height, weight, birthday)
            if success:
                st.success("Registrierung erfolgreich!")
                st.session_state['login_mode'] = True
                st.button("Zum Login", on_click=toggle_mode)
            else:
                st.error(f"Fehler: {err}")
        else:
            st.error("Es gibt Fehler in den Eingaben, bitte korrigieren Sie diese.")

if st.session_state.get('authenticated', False):
    st.success("Du bist eingeloggt!")

import streamlit as st
from datetime import datetime

def validate_username(username):
    if not username or len(username) < 3:
        st.error("Benutzername muss mindestens 3 Zeichen lang sein.")
        return False
    return True

def validate_email(email):
    if not email or "@" not in email or "." not in email.split("@")[-1]:
        st.error("Bitte geben Sie eine gültige E-Mail-Adresse ein.")
        return False
    return True

def validate_password(password):
    if not password or len(password) < 8:
        st.error("Passwort muss mindestens 8 Zeichen lang sein.")
        return False
    return True

def validate_height(height):
    if height <= 0:
        st.error("Größe muss größer als 0 m sein.")
        return False
    return True

def validate_weight(weight):
    if weight <= 0:
        st.error("Gewicht muss größer als 0 kg sein.")
        return False
    return True

def validate_birthday(birthday):
    min_birthday = datetime.strptime("1930-01-01", "%Y-%m-%d")
    max_birthday = datetime.strptime("2024-01-01", "%Y-%m-%d")
    birthday = datetime.strptime(birthday, "%Y-%m-%d")
    if not (min_birthday <= birthday <= max_birthday):
        st.error("Geburtsdatum muss zwischen dem 01.01.1930 und 01.01.2024 liegen.")
        return False
    return True

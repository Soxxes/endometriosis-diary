import streamlit as st

def pain_in_past():
    st.write("Aua in der Vergangenheit")

def pain_now():
    st.write("JETZT AUA")


def pain_diary():
    if not st.session_state['authenticated']:
        st.error("Bitte logge dich zunächst ein.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.button("Ich hatte Schmerzen", on_click=pain_in_past)
    with col2:
        st.button("Ich habe gerade Schmerzen", on_click=pain_now)


import streamlit as st
import requests


def pain_entry():
    if not st.session_state['authenticated']:
        st.error("Bitte logge dich zunächst ein.")
        return

    st.title("📝 Schmerz eintragen")

    with st.container():
        st.subheader("Aktueller Schmerzstatus")
        pain_is_now = st.checkbox("Ich habe jetzt Schmerzen.")
        
        if pain_is_now:
            st.write("💬 **Beschreibe deinen aktuellen Schmerz**")
        else:
            st.write("🕒 **Wann hattest du zuletzt Schmerzen?**")
        
        pain_strength = st.select_slider(
            "Wie stark ist dein Schmerz?",
            options=["leicht", "mittel", "stark"],
            help="Bewerte deinen Schmerz von leicht bis stark."
        )

        pain_location = st.multiselect(
            "Wo ist dein Schmerz? (Mehrfachauswahl möglich)",
            options=[
                "Unterleib",
                "Bauchbereich",
                "Brustkorb",
                "Kopf & Nacken"
            ]
        )
        
        if not pain_is_now:
            pain_time = st.radio(
                "Wann war dein Schmerz ungefähr?",
                options=["morgens", "mittags", "abends"],
                horizontal=True
            )

    st.markdown("---")

    if st.button("Eintrag speichern"):
        st.success("Dein Schmerzeintrag wurde erfolgreich gespeichert!")

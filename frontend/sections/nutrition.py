import os
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import openfoodfacts as off
from datetime import datetime, time


load_dotenv()

api = off.API(user_agent="Test/1.0")


def search_foods(query):
    # api_url = f"http://localhost:5000/api/foods/search?query={query}"
    # response = requests.get(api_url)
    # if response.status_code == 200:
    #     return response.json().get("results", [])
    # return []
    result = api.product.text_search(query)
    # print(len(result.get("products")))
    return result.get("products")[:15]

def dummy_search_foods(query):
    return [
        {
            "product_name": "Apfel",
            "brand": "Generic",
            "serving_size": "100g",
            "nutrients": {
                "calories": 52,
                "protein": 0.3,
                "carbs": 14,
                "fat": 0.2,
                "fiber": 2.4,
                "sugar": 10.3,
                "magnesium": 5,
                "potassium": 107
            }
        },
        {
            "product_name": "Apfelsaft",
            "brand": "Brand A",
            "serving_size": "250ml",
            "nutrients": {
                "calories": 46,
                "protein": 0.1,
                "carbs": 11,
                "fat": 0.1,
                "fiber": 0.2,
                "sugar": 10.1,
                "magnesium": 3,
                "potassium": 115
            }
        },
        {
            "product_name": "Banane",
            "brand": "Brand B",
            "serving_size": "250ml",
            "nutrients": {
                "calories": 46,
                "protein": 0.1,
                "carbs": 11,
                "fat": 0.1,
                "fiber": 0.2,
                "sugar": 10.1,
                "magnesium": 3,
                "potassium": 115
            }
        }
    ]


def add_food_entry(data):
    api_url = "http://localhost:5000/api/foodEntries/add"
    response = requests.post(api_url, json=data)
    if response.status_code == 201:
        return True, None
    return False, response.json().get("errors")


def nutrition_entry():
    st.title("🍎 Ernährungseintrag")
    user_id = st.session_state.user_id

    query = st.text_input("Suche nach Lebensmitteln")
    if query:
        search_results = search_foods(query)

        if search_results:
            food_options = {
                f"{result['product_name']}": result['nutriments']
                for result in search_results
            }

            # selectbox for the user to choose one or more foods
            selected_food = st.selectbox("Wähle ein Lebensmittel", food_options.keys())
            nutritions = food_options[selected_food]

            col1, col2 = st.columns([2, 1])
            with col1:
                portion_quantity = st.number_input("Menge", min_value=0.0, step=0.1)
            with col2:
                portion_unit = st.selectbox("Einheit", ["g", "kg"])

            if st.button("Lebensmittel hinzufügen"):
                st.session_state['selected_foods'].append({
                    "food_name": selected_food,
                    "quantity": portion_quantity,
                    "unit": portion_unit,
                    "nutrients": {key: value for key, value in nutritions.items() if type(value) in (float, int)}
                })
                print(nutritions)
                st.success(f"{selected_food} wurde zur Liste hinzugefügt!")

        else:
            st.write("Keine Ergebnisse gefunden.")

    if st.session_state['selected_foods']:
        st.write("Deine gewählten Lebensmittel:")
        for food in st.session_state['selected_foods']:
            st.write(f"- {food.get('food_name')} ({food.get('quantity')} {food.get('unit')})")

    st.markdown("## Aktivität")
    activity = st.select_slider("🏃 Wie aktiv warst du heute?",
                                options=(0, 1, 2, 3),
                                help="Bewerte deinen körperliche Aktivität von 'gar nicht' bis 'viel'.")

    st.markdown("## Sonstiges")
    fast_food = st.checkbox("🍔 Fast Food gegessen?")
    alcohol = st.checkbox("🍺 Alkohol getrunken?")

    st.markdown("---")

    entry_time = st.radio(
                "🕒 Tageszeit der Aufnahme",
                options=["morgens", "mittags", "abends"],
                horizontal=True
            )
    if entry_time == "morgens":
        # 9 am
        entry_time = time(9, 0)
    elif entry_time == "mittags":
        # 1 pm
        entry_time = time(13, 0)
    elif entry_time == "abends":
        # 6 pm
        entry_time = time(18, 0)

    entry_date = st.date_input("📅 Datum des Eintrags",
                               datetime.today())

    entry_datetime = datetime.combine(entry_date, entry_time).strftime(format="%Y-%m-%d %H:%M")
    entry_date = entry_date.strftime("%Y-%m-%d")

    if st.button("Eintrag speichern"):
        data = {
            "user_id": user_id,
            "foods": [food.get('food_name') for food in st.session_state['selected_foods']],
            # always in 'g' not 'kg'
            "portion_sizes": [food.get('quantity') * 1000 if food.get('unit') == "kg" else food.get('quantity')
                              for food in st.session_state['selected_foods']],
            "alcohol": alcohol,
            "activity": activity,
            "fast_food": fast_food,
            "date": entry_date,
            "meal_time_stamp": entry_datetime,
            "nutritions": [food.get('nutrients') for food in st.session_state['selected_foods']],
            "submit_time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        if len(data["foods"]) < 1:
            st.warning("Bitte gib mindestens ein Lebensmittel an.")
        else:
            success, error = add_food_entry(data)
            if success:
                st.session_state['selected_foods'] = []
                st.success("Eintrag gespeichert!")
                # st.rerun()
            else:
                st.warning(f"Ein Fehler ist aufgetreten: {error}")

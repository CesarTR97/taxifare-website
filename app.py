import streamlit as st
import requests
from datetime import datetime
import folium
from streamlit_folium import st_folium

st.title("Predicción de Tarifa de Taxi 🚖")

pickup_datetime_str = st.text_input("Fecha y hora del viaje (YYYY-MM-DD HH:MM:SS)", "2014-07-06 19:18:00")
pickup_longitude = st.number_input("Longitud de origen", value=-73.950655, format="%.6f")
pickup_latitude = st.number_input("Latitud de origen", value=40.783282, format="%.6f")
dropoff_longitude = st.number_input("Longitud de destino", value=-73.984365, format="%.6f")
dropoff_latitude = st.number_input("Latitud de destino", value=40.769802, format="%.6f")
passenger_count = st.number_input("Número de pasajeros", min_value=1, max_value=5, value=1)

url = 'https://wagon-data-tpl-image-173219828681.europe-west1.run.app/predict'

try:
    pickup_datetime = datetime.strptime(pickup_datetime_str, "%Y-%m-%d %H:%M:%S")
except:
    st.error("⚠️ Formato de fecha inválido. Usa 'YYYY-MM-DD HH:MM:SS'.")

pickup_coords = [pickup_latitude, pickup_longitude]
dropoff_coords = [dropoff_latitude, dropoff_longitude]

if pickup_longitude and pickup_latitude and dropoff_longitude and dropoff_latitude:
    m = folium.Map(location=[pickup_latitude, pickup_longitude], zoom_start=12)
    folium.Marker([pickup_latitude, pickup_longitude], tooltip="Origen", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([dropoff_latitude, dropoff_longitude], tooltip="Destino", icon=folium.Icon(color='blue')).add_to(m)
    st.subheader("Mapa del recorrido")
    st_folium(m, width=700, height=400)

if st.button("Predecir tarifa"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    try:
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        fare = response.json().get("fare")
        st.metric(label="Tarifa estimada (USD)", value=f"${fare:.2f}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error al contactar la API: {e}")

import streamlit as st
import requests
from datetime import datetime

# Weather API details (Use st.secrets for security)
API_KEY = st.secrets["API_KEY"]  # Store API key in Streamlit secrets
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Function to fetch current weather
def get_weather(city_name):
    params = {'q': city_name, 'appid': API_KEY, 'units': 'metric'}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function to fetch 5-day weather forecast
def get_forecast(city_name):
    params = {'q': city_name, 'appid': API_KEY, 'units': 'metric'}
    try:
        response = requests.get(FORECAST_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Streamlit UI
st.title("☀️ Weather Info - Current & 5-Day Forecast")

# City input
city_name = st.text_input("Enter City Name:")

if st.button("Check Weather") or city_name:
    weather_data = get_weather(city_name)
    
    if "error" in weather_data:
        st.error(f"Error fetching weather data: {weather_data['error']}")
    elif weather_data.get("cod") != 200:
        st.error(f"City '{city_name}' not found. Please check the name.")
    else:
        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"].capitalize()
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]
        wind_speed = weather_data["wind"]["speed"]
        icon_code = weather_data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        
        # Display weather info
        st.subheader(f"Current Weather in {city}, {country}")
        st.image(icon_url, caption=description)
        st.metric("🌡 Temperature", f"{temp}°C")
        st.metric("💨 Wind Speed", f"{wind_speed} m/s")
        st.metric("💧 Humidity", f"{humidity}%")
        st.metric("🌍 Pressure", f"{pressure} hPa")
        
        # Fetch and display forecast data
        forecast_data = get_forecast(city_name)
        if "list" in forecast_data:
            st.subheader("5-Day Weather Forecast")
            forecast_list = []
            for i in range(0, len(forecast_data["list"]), 8):
                entry = forecast_data["list"][i]
                date = datetime.utcfromtimestamp(entry["dt"]).strftime('%A, %d %B %Y')
                temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"].capitalize()
                forecast_list.append([date, f"{temp}°C", desc])
            
            st.table(forecast_list)
        else:
            st.error("Unable to fetch forecast data.")

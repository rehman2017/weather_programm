import streamlit as st
import requests
from datetime import datetime, timedelta

# Weather API URL and Key (replace with your actual API key)
API_KEY = '82b34f6ff105db2f350a21a4e8b32ca2'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Function to get weather data for the entered city
def get_weather(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'  # To get the temperature in Celsius
    }
    
    response = requests.get(BASE_URL, params=params)
    return response.json()

# Function to get 5-day weather forecast
def get_forecast(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'  # To get the temperature in Celsius
    }
    
    response = requests.get(FORECAST_URL, params=params)
    return response.json()

# Function to format the forecast data
def format_forecast_data(forecast_data):
    forecast_list = []
    if "list" in forecast_data:
        for i in range(0, len(forecast_data["list"]), 8):  # Each entry represents 3 hours, so we take every 8th one (24h = 8*3 hours)
            date = datetime.utcfromtimestamp(forecast_data["list"][i]["dt"])
            temp = forecast_data["list"][i]["main"]["temp"]
            description = forecast_data["list"][i]["weather"][0]["description"]
            forecast_list.append(f"{date.strftime('%A, %d %B %Y')} - Temp: {temp}°C, {description}")
    return forecast_list

# Streamlit UI
st.title(" Weather Info - Check Current & 5-Day Forecast")

# Input for the city name
city_name = st.text_input("Enter City Name:", "")

# Check weather button
check_weather_button = st.button("Check Weather")

# Show weather data on button click or when Enter is pressed
if (check_weather_button or city_name) and city_name:
    weather_data = get_weather(city_name)
    
    if weather_data.get("cod") != 200:
        st.error(f"City '{city_name}' not found, please check the name.")
    else:
        # Display the current weather
        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]
        wind_speed = weather_data["wind"]["speed"]
        weather_report = f"Weather in {city}, {country}:\nTemperature: {temp}°C\nDescription: {description}\nHumidity: {humidity}%\nPressure: {pressure} hPa\nWind Speed: {wind_speed} m/s"
        
        st.write("### Current Weather:")
        st.text(weather_report)
        
        # Get and display the 5-day weather forecast
        forecast_data = get_forecast(city_name)
        
        if "list" in forecast_data:
            st.write("### 5-Day Weather Forecast:")
            forecast_list = format_forecast_data(forecast_data)
            for forecast in forecast_list:
                st.write(forecast)
        else:
            st.error("Unable to fetch forecast data.")

# Instructions and UI message
st.write("### Instructions:")
st.write("1. Type the name of a city in the input box.")
st.write("2. Press **Enter** or click the **Check Weather** button to view the weather details.")
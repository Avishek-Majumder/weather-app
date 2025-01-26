import streamlit as st
import requests
from datetime import datetime

# Function to fetch current weather data using OpenWeatherMap API
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] != 200:
        return None
    
    weather_data = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "wind_direction": data["wind"]["deg"],
        "pressure": data["main"]["pressure"],
        "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M"),
        "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M"),
        "feels_like": data["main"]["feels_like"],
    }
    return weather_data

# Function to fetch 24-hour forecast (example using OpenWeatherMap)
def get_24h_forecast(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] != "200":
        return None
    
    forecast_data = []
    for item in data["list"][:6]:  # Get the next 6 entries (24-hour forecast)
        forecast_data.append({
            "time": datetime.fromtimestamp(item["dt"]).strftime("%H:%M"),
            "temperature": item["main"]["temp"],
            "wind_speed": item["wind"]["speed"],
        })
    return forecast_data

# Streamlit App
def main():
    st.title("🌦️ Interactive Weather App")
    
    # Input for city name
    city = st.text_input("Enter a city name:", "Chittagong")
    
    # Hardcode your API key here
    api_key = "70c9a23e74f932ea43574a53187adeb6"  # Replace with your API key
    
    if st.button("Get Weather"):
        if not api_key:
            st.error("Please enter a valid API key.")
        else:
            # Fetch current weather and 24-hour forecast
            weather_data = get_weather(city, api_key)
            forecast_data = get_24h_forecast(city, api_key)
            
            if weather_data and forecast_data:
                # Current Weather Section
                st.write(f"## Current Weather in {weather_data['city']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Temperature", f"{weather_data['temperature']}°C")
                    st.metric("Humidity", f"{weather_data['humidity']}%")
                with col2:
                    st.metric("Wind Speed", f"{weather_data['wind_speed']} m/s")
                    st.write(f"**Condition:** {weather_data['description'].capitalize()}")
                st.image(f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png")
                
                # Additional Details Section
                st.write("### Additional Details")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Real Feel", f"{weather_data['feels_like']}°C")
                    st.metric("Pressure", f"{weather_data['pressure']} hPa")
                with col2:
                    st.metric("Wind Direction", f"{weather_data['wind_direction']}°")
                    st.metric("Sunrise", f"{weather_data['sunrise']}")
                with col3:
                    st.metric("UV Index", "Weak")  # Placeholder, replace with actual UV data
                    st.metric("Sunset", f"{weather_data['sunset']}")
                
                # 24-Hour Forecast Section
                st.write("## 24-Hour Forecast")
                time = [f["time"] for f in forecast_data]
                temp = [f["temperature"] for f in forecast_data]
                wind = [f["wind_speed"] for f in forecast_data]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Temperature (°C)**")
                    st.line_chart(temp)
                with col2:
                    st.write("**Wind Speed (m/s)**")
                    st.line_chart(wind)
                
                # AQI Section (Placeholder)
                st.write("### Air Quality Index (AQI)")
                st.metric("AQI", "112")  # Replace with actual AQI data
                
                # Footer
                st.markdown("---")
                st.markdown("**This project was created by Avishek Majumder. All rights reserved.**")
            else:
                st.error("City not found. Please try again.")

if __name__ == "__main__":
    main()
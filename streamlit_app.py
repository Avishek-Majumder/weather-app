import streamlit as st
import requests

# Function to fetch weather data
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
    }
    return weather_data

# Streamlit App
def main():
    st.title("🌦️ Interactive Weather App")
    
    # Input for city name
    city = st.text_input("Enter a city name:", "London")
    
    # Hardcode your API key here or leave it as user input
    api_key = "70c9a23e74f932ea43574a53187adeb6"  # Replace with your API key
    
    if st.button("Get Weather"):
        if not api_key:
            st.error("Please enter a valid API key.")
        else:
            weather_data = get_weather(city, api_key)
            
            if weather_data:
                st.write(f"### Weather in {weather_data['city']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Temperature", f"{weather_data['temperature']}°C")
                    st.metric("Humidity", f"{weather_data['humidity']}%")
                with col2:
                    st.metric("Wind Speed", f"{weather_data['wind_speed']} m/s")
                    st.write(f"**Condition:** {weather_data['description'].capitalize()}")
                st.image(f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png")
            else:
                st.error("City not found. Please try again.")

if __name__ == "__main__":
    main()
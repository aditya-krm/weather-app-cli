import requests

def fetch_weather(location, api_key):
    """Fetches weather data from the OpenWeatherMap API for a given location."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "weather": data['weather'][0]['description'],
            "wind_speed": data['wind']['speed']
        }
        return weather_info
    else:
        print(f"Error fetching weather data: {response.status_code}")
        return None

# Extended weather query for forecast data
def fetch_weather_forecast(location, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Process forecast data (e.g., next 5 days)
        forecast_data = []
        for item in data['list']:
            forecast_data.append({
                "datetime": item['dt_txt'],
                "temperature": item['main']['temp'],
                "weather": item['weather'][0]['description']
            })
        return forecast_data
    else:
        print(f"Error fetching forecast data: {response.status_code}")
        return None

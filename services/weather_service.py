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

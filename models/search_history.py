import json

def store_search_history(connection, user_id, location, weather_data):
    """Stores the search history (weather data) for a user in the database."""
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO search_history (user_id, location, weather_data) VALUES (%s, %s, %s)",
        (user_id, location, json.dumps(weather_data))
    )
    connection.commit()
    cursor.close()

def view_search_history(connection, user_id):
    """Displays the user's search history."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT location, weather_data, timestamp FROM search_history WHERE user_id = %s", (user_id,))
    history = cursor.fetchall()

    if history:
        print("Search History:")
        for record in history:
            weather_data = json.loads(record['weather_data'])
            print(f"{record['timestamp']}: {record['location']}")
            print(f"  Temperature: {weather_data['temperature']}°C")
            print(f"  Humidity: {weather_data['humidity']}%")
            print(f"  Conditions: {weather_data['weather']}")
            print(f"  Wind Speed: {weather_data['wind_speed']} m/s\n")
    else:
        print("No search history found.")
    cursor.close()

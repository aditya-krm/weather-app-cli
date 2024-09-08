import json
from services.weather_service import fetch_weather

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

# Delete search history
def delete_search_history(connection, user_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM search_history WHERE user_id = %s", (user_id,))
        connection.commit()
        print("Search history deleted.")
    except mysql.connector.Error as err:
        print(f"Error deleting search history: {err}")
        connection.rollback()
    finally:
        cursor.close()

# Get previous searches and refetch weather
def refetch_weather_for_old_search(connection, user_id, api_key):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, location FROM search_history WHERE user_id = %s", (user_id,))
    searches = cursor.fetchall()

    if not searches:
        print("No previous searches found.")
        return

    print("Previous searches:")
    for search in searches:
        print(f"{search['id']}: {search['location']}")

    search_id = int(input("Enter the search ID to refetch weather: "))
    selected_search = next((s for s in searches if s['id'] == search_id), None)

    if selected_search:
        weather_data = fetch_weather(selected_search['location'], api_key)
        print(weather_data)
    else:
        print("Invalid search ID.")
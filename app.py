from db.db_connection import connect_to_db
from models.user_model import register_user, login_user
from models.search_history import store_search_history, view_search_history
from services.weather_service import fetch_weather
from config import API_KEY

def handle_weather_search(connection, user_id):
    """Handles user input for searching weather and storing history."""
    while True:
        location = input("\nEnter a location for weather search (or type 'history' to view search history, 'logout' to log out): ").strip()

        if location.lower() == "logout":
            break
        elif location.lower() == "history":
            view_search_history(connection, user_id)
        else:
            weather_data = fetch_weather(location, API_KEY)
            if weather_data:
                print(f"\nWeather in {location.capitalize()}:")
                print(f"  Temperature: {weather_data['temperature']}°C")
                print(f"  Humidity: {weather_data['humidity']}%")
                print(f"  Conditions: {weather_data['weather']}")
                print(f"  Wind Speed: {weather_data['wind_speed']} m/s\n")
                
                # Store the search in the database
                store_search_history(connection, user_id, location, weather_data)

def main_menu(connection):
    """Displays the main menu for the CLI and handles user registration and login."""
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register_user(connection)
        elif choice == "2":
            user_id = login_user(connection)
            if user_id:
                handle_weather_search(connection, user_id)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def main():
    """Entry point for the CLI application."""
    connection = connect_to_db()

    try:
        main_menu(connection)
    finally:
        connection.close()

if __name__ == "__main__":
    main()

from db.db_connection import connect_to_db
from models.user_model import register_user, login_user, update_profile
from models.search_history import store_search_history, view_search_history, delete_search_history, refetch_weather_for_old_search
from services.weather_service import fetch_weather, fetch_weather_forecast
from config import API_KEY

def handle_weather_search(connection, user_id):
    """Handles user input for searching weather and storing history."""
    while True:
        print("\nOptions:")
        print("  1. Search Weather")
        print("  2. View Search History")
        print("  3. Refetch Previous Search")
        print("  4. Delete Search History")
        print("  5. Update Profile")
        print("  6. 5-Day Forecast")
        print("  7. Logout")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            location = input("Enter location for weather search: ").strip()
            weather_data = fetch_weather(location, API_KEY)
            if weather_data:
                print(f"\nWeather in {location.capitalize()}:")
                print(f"  Temperature: {weather_data['temperature']}°C")
                print(f"  Humidity: {weather_data['humidity']}%")
                print(f"  Conditions: {weather_data['weather']}")
                print(f"  Wind Speed: {weather_data['wind_speed']} m/s\n")
                
                # Store the search in the database
                store_search_history(connection, user_id, location, weather_data)

        elif choice == "2":
            view_search_history(connection, user_id)

        elif choice == "3":
            refetch_weather_for_old_search(connection, user_id, API_KEY)

        elif choice == "4":
            delete_search_history(connection, user_id)

        elif choice == "5":
            update_profile(connection, user_id)

        elif choice == "6":
            location = input("Enter location for 5-day weather forecast: ").strip()
            forecast_data = fetch_weather_forecast(location, API_KEY)
            if forecast_data:
                print(f"\n5-Day Forecast for {location.capitalize()}:")
                for day in forecast_data:
                    print(f"  Date/Time: {day['datetime']}")
                    print(f"  Temperature: {day['temperature']}°C")
                    print(f"  Conditions: {day['weather']}\n")
        
        elif choice == "7":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")

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

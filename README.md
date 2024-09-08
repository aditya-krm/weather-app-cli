# Weather CLI Application

A command-line interface (CLI) application that allows users to register, log in, fetch weather information from OpenWeatherMap API, and view their search history.

## Table of Contents

- [Source Code Style](#source-code-style)
- [Setup Instructions](#setup-instructions)
- [API Usage](#api-usage)
- [Database Schema](#database-schema)
- [Design Decisions](#design-decisions)
- [Bonus asked](#bonus-asked)

## Source Code Style

```
/weather_app_cli
│
├── /models
│   ├── __init__.py         # Makes models a package
│   ├── user_model.py       # User registration and login
│   ├── search_history.py   # Search history operations
│
├── /services
│   ├── __init__.py         # Makes services a package
│   ├── weather_service.py  # Fetching weather data
│
├── /db
│   ├── __init__.py         # Makes db a package
│   └── db_connection.py    # Database connection
│
├── app.py                  # Main application logic
├── requirements.txt        # Python dependencies
└── config.py               # Configuration for API keys, etc.
└── schema.sql              # SQL schema for database

```

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd weather_cli_app
   ```

2. **Install dependencies:**

   Ensure you have Python 3.6 or higher installed. Create a virtual environment and install the required packages.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set up the database:**

   Import the provided SQL schema into your MySQL database. Replace the database credentials in `main.py` with your own.

   ```bash
   mysql -u <username> -p < database_name < schema.sql
   ```

4. **Obtain an API Key:**

   Sign up at [OpenWeatherMap](https://openweathermap.org/api) to get your API key. Replace `"your_openweathermap_api_key"` in `config.py` with your actual API key.

5. **Run the application:**

   ```bash
   python main.py
   ```

## API Usage

The application interacts with the OpenWeatherMap API to fetch weather data. The endpoint used is:

- **GET** `http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric`

**Parameters:**

- `q`: Location (city name)
- `appid`: Your OpenWeatherMap API key
- `units`: Metric for temperature in Celsius

## Database Schema

The application uses two tables: `users` and `search_history`.

**`users` Table:**

| Column     | Type      | Description                      |
| ---------- | --------- | -------------------------------- |
| `id`       | INT       | Primary Key, auto-incremented ID |
| `username` | VARCHAR   | Unique username for login        |
| `password` | VARBINARY | Hashed password                  |

**`search_history` Table:**

| Column         | Type      | Description                      |
| -------------- | --------- | -------------------------------- |
| `id`           | INT       | Primary Key, auto-incremented ID |
| `user_id`      | INT       | Foreign Key to `users` table     |
| `location`     | VARCHAR   | Location searched by the user    |
| `weather_data` | TEXT      | JSON-encoded weather data        |
| `timestamp`    | TIMESTAMP | Time of the search               |

## Design Decisions

1. **Security:**

   - Passwords are hashed using bcrypt for secure storage.
   - API keys and sensitive information are not hard-coded; replace placeholders with your actual credentials.

2. **Error Handling:**

   - Basic error handling is implemented for database operations and API requests.

3. **User Experience:**

   - The CLI interface allows users to register, log in, and interact with weather data intuitively.

4. **Scalability:**

   - The application is designed to be simple but can be expanded with additional features such as user profile management or more detailed weather analytics.

5. **Database:**
   - MySQL is used for persistent storage due to its reliability and ease of use.

## Bonus asked

- Implement a feature allowing users to delete specific entries from their search history.
- Add functionality to allow users to update their profile information (e.g., username,
  password).
- Extend the application to support additional weather-related queries, such as a 5-day
  forecast.

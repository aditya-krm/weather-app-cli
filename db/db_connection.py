import mysql.connector

def connect_to_db():
    """Establish a connection to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="sss_assignment_sep24",
        password="doitnow ",
        database="weather_db"
    )

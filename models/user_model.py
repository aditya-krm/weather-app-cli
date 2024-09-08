import bcrypt
from getpass import getpass

def register_user(connection):
    """Registers a new user by storing hashed credentials (using bcrypt) in the database."""
    cursor = connection.cursor()
    username = input("Enter a new username: ")
    password = getpass("Enter a new password: ")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()
        print("Registration successful. You can now log in.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def login_user(connection):
    """Logs in a user by verifying credentials."""
    cursor = connection.cursor(dictionary=True)
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        print("Login successful!", user["username"])
        return user['id']
    else:
        print("Invalid username or password.")
        return None

    cursor.close()

# update profile details
def update_profile(connection, user_id):
    cursor = connection.cursor()
    new_username = input("Enter a new username: ")
    new_password = getpass("Enter a new password: ")
    
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("UPDATE users SET username = %s, password = %s WHERE id = %s", (new_username, hashed_password, user_id))
        connection.commit()
        print("Profile updated successfully.")
    except mysql.connector.Error as err:
        print(f"Error updating profile: {err}")
        connection.rollback()
    finally:
        cursor.close()
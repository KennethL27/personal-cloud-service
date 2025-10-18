# 001_initial_schema
import os
from dotenv import load_dotenv

def up(conn):
    load_dotenv()
    first_user_email = os.getenv("FIRST_USER_EMAIL", "first.last@example.com")
    first_user_name = os.getenv("FIRST_USER_NAME", "First Last")

    conn.executescript("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            is_admin BOOLEAN DEFAULT FALSE,
            is_guest BOOLEAN DEFAULT FALSE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            hard_drive_path_selection TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    conn.execute(
        "INSERT INTO users (email, name, is_admin, is_guest) VALUES (:email, :name, :is_admin, :is_guest);",
        {"email": first_user_email, "name": first_user_name, "is_admin": 1, "is_guest": 0}
    )
    conn.commit()

def down(conn):
    conn.executescript("""
        DROP TABLE user_settings;
        DROP TABLE users;
    """)
    conn.commit()
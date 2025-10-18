import sqlite3

def get_connection(db_path: str = "personal_cloud.db") -> sqlite3.Connection:
    conn = sqlite3.Connection(db_path)
    conn.row_factory = sqlite3.Row  # This allows dict-like access to rows
    return conn

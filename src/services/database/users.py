from src.services.database.db_service import get_connection

class User:
    def __init__(self, row, cursor):
        if row is not None:
            # Set each column as an attribute with its name from the cursor description
            for idx, col in enumerate(cursor.description):
                setattr(self, col[0], row[idx])

def get_user_by_id(id: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                        SELECT *
                        FROM users AS u
                        WHERE u.id = :user_id
                    """,
                    {
                        "user_id" : id
                    })
        
        user = cursor.fetchone()

        if user is None:
            return None

        return User(user, cursor)

def get_user_by_email(email: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                        SELECT *
                        FROM users AS u
                        WHERE u.email = :email
                    """,
                    {
                        "email" : email
                    })
        
        user = cursor.fetchone()

        if user is None:
            return None

        return User(user, cursor)
        
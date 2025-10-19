from datetime import datetime, timezone
from src.services.database.db_service import get_connection

class UserSetting:
    def __init__(self, row, cursor):
        if row is not None:
            # Set each column as an attribute with its name from the cursor description
            for idx, col in enumerate(cursor.description):
                setattr(self, col[0], row[idx])

def get_user_setting(id: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                    SELECT *
                    FROM user_settings AS us
                    WHERE us.user_id = :user_id
                """,
                {
                    "user_id" : id
                })
        
        user_setting = cursor.fetchone()

        if user_setting is None:
            return None

        return UserSetting(user_setting, cursor)

def create_user_setting(parameters):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                INSERT INTO user_settings (user_id, hard_drive_path_selection) 
                VALUES (:user_id, :hard_drive_path_selection)
                """,
                parameters
                )

        conn.commit()

def update_user_setting(parameters):
    with get_connection() as conn:
        cursor = conn.cursor()
        parameters["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
                UPDATE user_settings
                SET hard_drive_path_selection = :hard_drive_path_selection, updated_at = :updated_at
                WHERE user_id = :user_id 
                """,
                parameters
                )
        
        conn.commit()
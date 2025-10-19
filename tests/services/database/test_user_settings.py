from unittest.mock import patch, MagicMock
from src.services.database.user_settings import get_user_setting, create_user_setting, update_user_setting

class TestUserSettingsService:
    def test_get_user_setting__success(self):
        mock_row = (1, 1, "/Volumes/Drive1", "2024-01-01 10:00:00", "2024-01-01 10:00:00")
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id", None, None, None, None, None, None),
            ("user_id", None, None, None, None, None, None),
            ("hard_drive_path_selection", None, None, None, None, None, None),
            ("created_at", None, None, None, None, None, None),
            ("updated_at", None, None, None, None, None, None)
        ]
        mock_cursor.fetchone.return_value = mock_row
        
        with patch('src.services.database.user_settings.get_connection') as mock_get_conn:
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            user_setting = get_user_setting("1")
            
            assert user_setting is not None
            assert user_setting.id == 1
            assert user_setting.user_id == 1
            assert user_setting.hard_drive_path_selection == "/Volumes/Drive1"
            mock_cursor.execute.assert_called_once()

    def test_get_user_setting__not_found(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        with patch('src.services.database.user_settings.get_connection') as mock_get_conn:
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            user_setting = get_user_setting("999")
            
            assert user_setting is None

    def test_create_user_setting__success(self):
        mock_cursor = MagicMock()
        
        parameters = {
            "user_id": "1",
            "hard_drive_path_selection": "/Volumes/Drive1"
        }
        
        with patch('src.services.database.user_settings.get_connection') as mock_get_conn:
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            create_user_setting(parameters)
            
            assert mock_cursor.execute.call_count == 1
            assert mock_conn.commit.call_count == 1
            
            # Verify the SQL query was called with correct parameters
            call_args = mock_cursor.execute.call_args
            sql_query = call_args[0][0]
            query_params = call_args[0][1]
            
            assert "INSERT INTO user_settings" in sql_query
            assert query_params["user_id"] == "1"
            assert query_params["hard_drive_path_selection"] == "/Volumes/Drive1"

    def test_update_user_setting__success(self):
        mock_cursor = MagicMock()
        
        parameters = {
            "user_id": "1",
            "hard_drive_path_selection": "/Volumes/Drive2"
        }
        
        with patch('src.services.database.user_settings.get_connection') as mock_get_conn, \
             patch('src.services.database.user_settings.datetime') as mock_datetime:
            
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            # Mock current datetime
            mock_now = MagicMock()
            mock_now.strftime.return_value = "2024-01-01 10:30:00.000"
            mock_datetime.now.return_value = mock_now
            
            update_user_setting(parameters)
            
            assert mock_cursor.execute.call_count == 1
            assert mock_conn.commit.call_count == 1
            
            # Verify the SQL query was called with correct parameters
            call_args = mock_cursor.execute.call_args
            sql_query = call_args[0][0]
            query_params = call_args[0][1]
            
            assert "UPDATE user_settings" in sql_query
            assert "SET hard_drive_path_selection = :hard_drive_path_selection" in sql_query
            assert "updated_at = :updated_at" in sql_query
            assert "WHERE user_id = :user_id" in sql_query
            
            assert query_params["user_id"] == "1"
            assert query_params["hard_drive_path_selection"] == "/Volumes/Drive2"
            assert "updated_at" in query_params

    def test_update_user_setting__adds_updated_at(self):
        mock_cursor = MagicMock()
        
        parameters = {
            "user_id": "1",
            "hard_drive_path_selection": "/Volumes/Drive3"
        }
        
        with patch('src.services.database.user_settings.get_connection') as mock_get_conn, \
             patch('src.services.database.user_settings.datetime') as mock_datetime:
            
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            mock_now = MagicMock()
            mock_now.strftime.return_value = "2024-01-01 11:00:00"
            mock_datetime.now.return_value = mock_now
            
            update_user_setting(parameters)
            
            # Verify updated_at was added to parameters
            call_args = mock_cursor.execute.call_args
            query_params = call_args[0][1]
            
            assert query_params["updated_at"] == "2024-01-01 11:00:00"
            assert query_params["user_id"] == "1"
            assert query_params["hard_drive_path_selection"] == "/Volumes/Drive3"

    def test_user_setting_class_attributes(self):
        mock_row = (5, 2, "/Volumes/Drive4", "2024-01-01 09:00:00", "2024-01-01 09:15:00")
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id", None, None, None, None, None, None),
            ("user_id", None, None, None, None, None, None),
            ("hard_drive_path_selection", None, None, None, None, None, None),
            ("created_at", None, None, None, None, None, None),
            ("updated_at", None, None, None, None, None, None)
        ]
        
        from src.services.database.user_settings import UserSetting
        user_setting = UserSetting(mock_row, mock_cursor)
        
        assert user_setting.id == 5
        assert user_setting.user_id == 2
        assert user_setting.hard_drive_path_selection == "/Volumes/Drive4"
        assert user_setting.created_at == "2024-01-01 09:00:00"
        assert user_setting.updated_at == "2024-01-01 09:15:00"

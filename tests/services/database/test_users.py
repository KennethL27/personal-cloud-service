from unittest.mock import patch, MagicMock
from src.services.database.users import get_user_by_id, get_user_by_email

class TestUsersService:
    def test_get_user_by_id__success(self):
        mock_row = (1, "test@example.com", "Test User", 0, 0, "2024-01-01 10:00:00")
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id", None, None, None, None, None, None),
            ("email", None, None, None, None, None, None),
            ("name", None, None, None, None, None, None),
            ("is_admin", None, None, None, None, None, None),
            ("is_guest", None, None, None, None, None, None),
            ("created_at", None, None, None, None, None, None)
        ]
        mock_cursor.fetchone.return_value = mock_row
        
        with patch('src.services.database.users.get_connection') as mock_get_conn:
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            user = get_user_by_id("1")
            
            assert user is not None
            assert user.id == 1
            assert user.email == "test@example.com"
            assert user.name == "Test User"
            mock_cursor.execute.assert_called_once()

    def test_get_user_by_id__not_found(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        with patch('src.services.database.users.get_connection') as mock_get_conn:
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            user = get_user_by_id("999")
            
            assert user is None

    def test_get_user_by_email__success(self):
        mock_row = (1, "test@example.com", "Test User", 0, 0, "2024-01-01 10:00:00")
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id", None, None, None, None, None, None),
            ("email", None, None, None, None, None, None),
            ("name", None, None, None, None, None, None),
            ("is_admin", None, None, None, None, None, None),
            ("is_guest", None, None, None, None, None, None),
            ("created_at", None, None, None, None, None, None)
        ]
        mock_cursor.fetchone.return_value = mock_row
        
        with patch('src.services.database.users.get_connection') as mock_get_conn:
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            user = get_user_by_email("test@example.com")
            
            assert user is not None
            assert user.id == 1
            assert user.email == "test@example.com"
            assert user.name == "Test User"
            mock_cursor.execute.assert_called_once()

    def test_get_user_by_email__not_found(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        with patch('src.services.database.users.get_connection') as mock_get_conn:
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            user = get_user_by_email("nonexistent@example.com")
            
            assert user is None
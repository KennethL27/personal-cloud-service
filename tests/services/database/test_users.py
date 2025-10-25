from unittest.mock import patch, MagicMock
from src.services.database.users import User, create_user, get_user_by_id, get_user_by_email, update_user

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

    def test_create_user__success(self):
        """Test creating a new user successfully"""
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id", None, None, None, None, None, None),
            ("email", None, None, None, None, None, None),
            ("name", None, None, None, None, None, None),
            ("is_admin", None, None, None, None, None, None),
            ("is_guest", None, None, None, None, None, None),
            ("created_at", None, None, None, None, None, None)
        ]
        
        mock_new_user = MagicMock()
        mock_new_user.id = 5
        mock_new_user.email = "newuser@example.com"
        mock_new_user.name = "New User"
        mock_new_user.is_admin = False
        mock_new_user.is_guest = True
        
        parameters = {
            "email": "newuser@example.com",
            "name": "New User", 
            "is_admin": False,
            "is_guest": True
        }
        
        with patch('src.services.database.users.get_connection') as mock_get_conn, \
             patch('src.services.database.users.get_user_by_email', return_value=mock_new_user) as mock_get_by_email:
            
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            result = create_user(parameters)
            
            assert result == mock_new_user
            assert mock_cursor.execute.call_count == 1
            assert mock_conn.commit.call_count == 1
            
            # Verify the SQL query was called with correct parameters
            call_args = mock_cursor.execute.call_args
            sql_query = call_args[0][0]
            query_params = call_args[0][1]
            
            assert "INSERT INTO users" in sql_query
            assert "VALUES (:email, :name, :is_admin, :is_guest)" in sql_query
            assert query_params["email"] == "newuser@example.com"
            assert query_params["name"] == "New User"
            assert query_params["is_admin"] == False
            assert query_params["is_guest"] == True
            
            # Verify get_user_by_email was called to return the created user
            mock_get_by_email.assert_called_once_with("newuser@example.com")

    def test_update_user__success(self):
        """Test updating an existing user successfully"""
        mock_cursor = MagicMock()
        
        parameters = {
            "email": "updated@example.com",
            "name": "Updated User",
            "is_admin": True,
            "is_guest": False
        }
        
        with patch('src.services.database.users.get_connection') as mock_get_conn, \
             patch('src.services.database.users.datetime') as mock_datetime:
            
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            # Mock current datetime
            mock_now = MagicMock()
            mock_datetime.now.return_value = mock_now
            
            update_user(parameters)
            
            assert mock_cursor.execute.call_count == 1
            assert mock_conn.commit.call_count == 1
            
            # Verify the SQL query was called with correct parameters
            call_args = mock_cursor.execute.call_args
            sql_query = call_args[0][0]
            query_params = call_args[0][1]
            
            assert "UPDATE users" in sql_query
            assert "SET email = :email, name = :name" in sql_query
            assert "is_admin = :is_admin, is_guest = :is_guest" in sql_query
            
            assert query_params["email"] == "updated@example.com"
            assert query_params["name"] == "Updated User"
            assert query_params["is_admin"] == True
            assert query_params["is_guest"] == False

    def test_user_class_attributes(self):
        """Test User class properly sets attributes from database row"""
        mock_row = (10, "test@example.com", "Test User", 1, 0, "2024-01-01 10:00:00")
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id", None, None, None, None, None, None),
            ("email", None, None, None, None, None, None),
            ("name", None, None, None, None, None, None),
            ("is_admin", None, None, None, None, None, None),
            ("is_guest", None, None, None, None, None, None),
            ("created_at", None, None, None, None, None, None)
        ]
        
        user = User(mock_row, mock_cursor)
        
        assert user.id == 10
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.is_admin == 1
        assert user.is_guest == 0
        assert user.created_at == "2024-01-01 10:00:00"

    def test_user_class_none_row(self):
        """Test User class handles None row gracefully"""
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id", None, None, None, None, None, None),
            ("email", None, None, None, None, None, None)
        ]
        
        user = User(None, mock_cursor)
        
        # When row is None, no attributes should be set
        assert not hasattr(user, 'id')
        assert not hasattr(user, 'email')
from unittest.mock import patch, MagicMock

class TestShareAPI:
    def test_share__create_new_user_success(self, test_client, bypass_auth):
        """Test sharing with a new user (user doesn't exist yet)"""
        # Mock admin user
        mock_admin_user = MagicMock()
        mock_admin_user.is_admin = True
        
        # Mock non-existent user lookup
        mock_new_user = MagicMock()
        mock_new_user.id = 2
        
        payload = {
            "name": "John Doe",
            "email": "john@example.com", 
            "hard_drive_path_selection": "/Volumes/Drive1"
        }
        
        with patch('src.api.permissions.share.get_user_by_email') as mock_get_user_by_email, \
             patch('src.api.permissions.share.create_user', return_value=mock_new_user) as mock_create_user, \
             patch('src.api.permissions.share.create_user_setting') as mock_create_setting:
            
            # Mock admin user lookup
            mock_get_user_by_email.side_effect = lambda email: mock_admin_user if email == "test@gmail.com" else None
            
            response = test_client.put("/permissions/share/", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            
            # Verify new user was created
            mock_create_user.assert_called_once_with({
                "email": "john@example.com",
                "name": "John Doe",
                "is_admin": False,
                "is_guest": True
            })
            
            # Verify user setting was created
            mock_create_setting.assert_called_once_with({
                "user_id": 2,
                "hard_drive_path_selection": "/Volumes/Drive1"
            })

    def test_share__update_existing_user_success(self, test_client, bypass_auth):
        """Test sharing with an existing user"""
        # Mock admin user
        mock_admin_user = MagicMock()
        mock_admin_user.is_admin = True
        
        # Mock existing user
        mock_existing_user = MagicMock()
        mock_existing_user.id = 3
        mock_existing_user.email = "jane@example.com"
        
        payload = {
            "name": "Jane Smith", 
            "email": "jane@example.com",
            "hard_drive_path_selection": "/Volumes/Drive2"
        }
        
        with patch('src.api.permissions.share.get_user_by_email') as mock_get_user_by_email, \
             patch('src.api.permissions.share.update_user') as mock_update_user, \
             patch('src.api.permissions.share.get_user_setting', return_value=None), \
             patch('src.api.permissions.share.create_user_setting') as mock_create_setting:
            
            # Mock user lookups - return admin for current user, existing user for payload email
            mock_get_user_by_email.side_effect = lambda email: {
                "test@gmail.com": mock_admin_user,
                "jane@example.com": mock_existing_user
            }.get(email)
            
            response = test_client.put("/permissions/share/", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            
            # Verify user was updated
            mock_update_user.assert_called_once_with({
                "email": "jane@example.com",
                "name": "Jane Smith",
                "is_admin": False,
                "is_guest": True
            })
            
            # Verify user setting was created (since get_user_setting returned None)
            mock_create_setting.assert_called_once_with({
                "user_id": 3,
                "hard_drive_path_selection": "/Volumes/Drive2"
            })

    def test_share__update_existing_user_with_settings(self, test_client, bypass_auth):
        """Test sharing with an existing user who already has settings"""
        # Mock admin user
        mock_admin_user = MagicMock()
        mock_admin_user.is_admin = True
        
        # Mock existing user with settings
        mock_existing_user = MagicMock()
        mock_existing_user.id = 4
        mock_existing_user.email = "bob@example.com"
        
        mock_user_setting = MagicMock()
        
        payload = {
            "name": "Bob Wilson",
            "email": "bob@example.com", 
            "hard_drive_path_selection": "/Volumes/Drive3"
        }
        
        with patch('src.api.permissions.share.get_user_by_email') as mock_get_user_by_email, \
             patch('src.api.permissions.share.update_user') as mock_update_user, \
             patch('src.api.permissions.share.get_user_setting', return_value=mock_user_setting), \
             patch('src.api.permissions.share.update_user_setting') as mock_update_setting:
            
            # Mock user lookups
            mock_get_user_by_email.side_effect = lambda email: {
                "test@gmail.com": mock_admin_user,
                "bob@example.com": mock_existing_user
            }.get(email)
            
            response = test_client.put("/permissions/share/", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            
            # Verify user setting was updated (not created)
            mock_update_setting.assert_called_once_with({
                "user_id": 4,
                "hard_drive_path_selection": "/Volumes/Drive3"
            })

    def test_share__unauthorized_non_admin(self, test_client, bypass_auth):
        """Test sharing fails when current user is not admin"""
        # Mock non-admin user
        mock_user = MagicMock()
        mock_user.is_admin = False
        
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "hard_drive_path_selection": "/Volumes/Drive1"
        }
        
        with patch('src.api.permissions.share.get_current_user', return_value={"email": "user@test.com"}), \
             patch('src.api.permissions.share.get_user_by_email', return_value=mock_user):
            
            response = test_client.put("/permissions/share/", json=payload)
            
            assert response.status_code == 401
            data = response.json()
            assert data["detail"] == "Unauthorized sharing access"

    def test_share__invalid_payload(self, test_client, bypass_auth):
        """Test sharing with invalid payload"""
        # Mock admin user
        mock_admin_user = MagicMock()
        mock_admin_user.is_admin = True
        
        with patch('src.api.permissions.share.get_current_user', return_value={"email": "admin@test.com"}), \
             patch('src.api.permissions.share.get_user_by_email', return_value=mock_admin_user):
            
            # Missing required fields
            response = test_client.put("/permissions/share/", json={})
            
            assert response.status_code == 422
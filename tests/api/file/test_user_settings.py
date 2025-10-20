from unittest.mock import patch, MagicMock
from src.services.database.user_settings import UserSetting

class TestUserSettingsAPI:
    def test_create_user_settings__success(self, test_client, bypass_auth):
        mock_user = MagicMock()
        mock_user.id = 1
        
        payload = {"hard_drive_path_selection": "/Volumes/Drive1"}
        
        with patch('src.api.file.user_settings.get_user_by_email', return_value=mock_user), \
             patch('src.api.file.user_settings.get_user_setting', return_value=None), \
             patch('src.api.file.user_settings.create_user_setting') as mock_create:
            
            response = test_client.put("/file/user_settings/", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            mock_create.assert_called_once_with({
                "user_id": 1,
                "hard_drive_path_selection": "/Volumes/Drive1"
            })

    def test_update_user_settings__success(self, test_client, bypass_auth):
        mock_user = MagicMock()
        mock_user.id = 1
        
        mock_user_setting = MagicMock()
        
        payload = {"hard_drive_path_selection": "/Volumes/Drive2"}
        
        with patch('src.api.file.user_settings.get_user_by_email', return_value=mock_user), \
             patch('src.api.file.user_settings.get_user_setting', return_value=mock_user_setting), \
             patch('src.api.file.user_settings.update_user_setting') as mock_update:
            
            response = test_client.put("/file/user_settings/", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            mock_update.assert_called_once_with({
                "user_id": 1,
                "hard_drive_path_selection": "/Volumes/Drive2"
            })

    def test_create_user_settings__user_not_found(self, test_client, bypass_auth):
        with patch('src.api.file.user_settings.get_user_by_email', return_value=None):
            response = test_client.put("/file/user_settings/", json={"hard_drive_path_selection": "/Volumes/Drive1"})
            
            assert response.status_code == 404
            data = response.json()
            assert data["detail"] == "User not found"

    def test_get_user_settings__success(self, test_client, bypass_auth):
        mock_row = (1, 1, "/Volumes/Drive1", "2024-01-01 10:00:00", "2024-01-01 10:00:00")
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id", None, None, None, None, None, None),
            ("user_id", None, None, None, None, None, None), 
            ("hard_drive_path_selection", None, None, None, None, None, None),
            ("created_at", None, None, None, None, None, None),
            ("updated_at", None, None, None, None, None, None)
        ]
        
        mock_user_setting = UserSetting(mock_row, mock_cursor)
        
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch('src.api.file.user_settings.get_user_by_email', return_value=mock_user), \
             patch('src.api.file.user_settings.get_user_setting', return_value=mock_user_setting):
            
            response = test_client.get("/file/user_settings/")
            
            assert response.status_code == 200
            data = response.json()
            assert data["hard_drive_path_selection"] == "/Volumes/Drive1"
            assert data["user_id"] == 1

    def test_get_user_settings__user_not_found(self, test_client, bypass_auth):
        with patch('src.api.file.user_settings.get_user_by_email', return_value=None):
            response = test_client.get("/file/user_settings/")
            
            assert response.status_code == 404
            data = response.json()
            assert data["detail"] == "User not found"

    def test_get_user_settings__no_settings(self, test_client, bypass_auth):
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch('src.api.file.user_settings.get_user_by_email', return_value=mock_user), \
             patch('src.api.file.user_settings.get_user_setting', return_value=None):
            
            response = test_client.get("/file/user_settings/")
            
            assert response.status_code == 200
            assert response.json() is None

from unittest.mock import patch, MagicMock
from pathlib import Path

def dummy_iter(content: bytes):
    return (chunk for chunk in [content])


class TestFileStream:
    def test_stream_video_file(self, test_client, bypass_auth):
        # Mock user and user settings
        mock_user = MagicMock()
        mock_user.id = 1
        
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/Volumes/TestDrive"
        
        with patch('src.api.file.stream.get_user_by_email', return_value=mock_user), \
             patch('src.api.file.stream.get_user_setting', return_value=mock_user_setting), \
             patch('src.api.file.stream.iterfile', return_value=dummy_iter(b"\x00\x00\x00\x20ftypisom")), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.resolve') as mock_resolve:
            
            # Mock the resolved path
            mock_path = MagicMock()
            mock_resolve.return_value = mock_path
            
            response = test_client.get("/file/stream/?file_name=videos/video.mp4")
            assert response.status_code == 200
            # assert response.headers["content-type"].startswith("video/")
            assert response.content == b"\x00\x00\x00\x20ftypisom"

    def test_stream_photo_file(self, test_client, bypass_auth):
        # Mock user and user settings
        mock_user = MagicMock()
        mock_user.id = 1
        
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/Volumes/TestDrive"
        
        with patch('src.api.file.stream.get_user_by_email', return_value=mock_user), \
             patch('src.api.file.stream.get_user_setting', return_value=mock_user_setting), \
             patch('src.api.file.stream.iterfile', return_value=dummy_iter(b"\xff\xd8\xff\xe0")), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.resolve') as mock_resolve:
            
            # Mock the resolved path
            mock_path = MagicMock()
            mock_resolve.return_value = mock_path
            
            response = test_client.get("/file/stream/?file_name=photos/photo.jpg")
            assert response.status_code == 200
            # assert response.headers["content-type"].startswith("image/")
            assert response.content == b"\xff\xd8\xff\xe0"

    def test_file_not_found(self, test_client, bypass_auth):
        # Mock user and user settings
        mock_user = MagicMock()
        mock_user.id = 1
        
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/Volumes/TestDrive"
        
        with patch('src.api.file.stream.get_user_by_email', return_value=mock_user), \
             patch('src.api.file.stream.get_user_setting', return_value=mock_user_setting), \
             patch.object(Path, 'exists', return_value=False):
            
            response = test_client.get("/file/stream/?file_name=photos/missing.jpg")
            assert response.status_code == 404
            assert response.json() == {"detail": "File not found"}

    def test_user_not_found(self, test_client, bypass_auth):
        with patch('src.api.file.stream.get_user_by_email', return_value=None):
            response = test_client.get("/file/stream/?file_name=photos/photo.jpg")
            assert response.status_code == 404
            assert response.json() == {"detail": "User not found"}

    def test_user_setting_not_found(self, test_client, bypass_auth):
        # Mock user but no user settings
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch('src.api.file.stream.get_user_by_email', return_value=mock_user), \
             patch('src.api.file.stream.get_user_setting', return_value=None):
            
            response = test_client.get("/file/stream/?file_name=photos/photo.jpg")
            assert response.status_code == 404
            assert response.json() == {"detail": "Default Path Section not found"}
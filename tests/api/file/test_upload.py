import pytest
from tempfile import NamedTemporaryFile
from unittest.mock import patch, MagicMock

class TestFileUpload:
    def test_file_upload(self, test_client):
        # Create a mock file object that can be used as a context manager
        mock_file_obj = MagicMock()
        mock_file_obj.__enter__ = MagicMock(return_value=mock_file_obj)
        mock_file_obj.__exit__ = MagicMock(return_value=None)
        
        with patch("src.api.file.upload.get_external_drive_path", return_value="/fake_drive/"), \
             patch("src.api.file.upload.get_folder_destination", return_value="/photos"), \
             patch("src.api.file.upload.os.makedirs", return_value=None), \
             patch("src.api.file.upload.shutil.copyfileobj", return_value=None), \
             patch("src.api.file.upload.open", return_value=mock_file_obj):
            mock_file = NamedTemporaryFile(suffix='.jpeg')
            response = test_client.post("/file/upload", files = {"files": mock_file})

            assert response.json() == {"uploaded_files": [mock_file.name.rsplit('/',1)[1]]}

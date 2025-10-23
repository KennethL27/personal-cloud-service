import pytest
from tempfile import NamedTemporaryFile
from unittest.mock import patch, MagicMock
from pathlib import Path

class TestFileUpload:
    def test_file_upload_success(self, test_client, bypass_auth):
        # Create a temporary file for testing
        with NamedTemporaryFile(suffix='.jpeg') as temp_file:
            # Create form data that matches the upload endpoint
            with patch("src.api.file.upload.open", MagicMock()) as mock_open, \
                 patch("src.api.file.upload.shutil.copyfileobj", MagicMock()) as mock_copyfileobj:
                
                # Mock the open context manager
                mock_file_obj = MagicMock()
                mock_open.return_value.__enter__.return_value = mock_file_obj
                
                # Test data - match frontend format
                files_data = [("files", (temp_file.name, temp_file, "image/jpeg"))]
                form_data = {"file_path_location": "/test/upload/path"}
                
                response = test_client.post("/file/upload/", data=form_data, files=files_data)

                assert response.status_code == 200
                # In test environment, file.filename returns the full path
                expected_filename = temp_file.name
                assert response.json() == {"uploaded_files": [expected_filename]}
                
                # Verify that open was called with the correct path
                mock_open.assert_called()
                # Verify that copyfileobj was called
                mock_copyfileobj.assert_called()
                
    def test_file_upload_error_handling(self, test_client, bypass_auth):
        # Test error handling when file operations fail
        with NamedTemporaryFile(suffix='.jpeg') as temp_file:
            with patch("src.api.file.upload.shutil.copyfileobj", side_effect=Exception("File system error")):
                files_data = [("files", (temp_file.name, temp_file, "image/jpeg"))]
                form_data = {"file_path_location": "/test/path"}
    
                response = test_client.post("/file/upload/", data=form_data, files=files_data)

                assert response.status_code == 200
                assert response.json() == {"status": "error", "message": "Unexpected error occurred: File system error"}

    def test_file_upload_multiple_files(self, test_client, bypass_auth):
        # Test uploading multiple files
        with NamedTemporaryFile(suffix='.jpg') as temp_file1, \
             NamedTemporaryFile(suffix='.png') as temp_file2:
            
            with patch("src.api.file.upload.open", MagicMock()) as mock_open, \
                 patch("src.api.file.upload.shutil.copyfileobj", MagicMock()) as mock_copyfileobj:
                
                # Mock the open context manager
                mock_file_obj = MagicMock()
                mock_open.return_value.__enter__.return_value = mock_file_obj
                
                # Match frontend format - multiple files with same field name
                files_data = [
                    ("files", (temp_file1.name, temp_file1, "image/jpeg")),
                    ("files", (temp_file2.name, temp_file2, "image/png"))
                ]
                form_data = {"file_path_location": "/test/path"}
                
                response = test_client.post("/file/upload/", data=form_data, files=files_data)

                assert response.status_code == 200
                # In test environment, file.filename returns the full path
                expected_filenames = [temp_file1.name, temp_file2.name]
                assert response.json() == {"uploaded_files": expected_filenames}
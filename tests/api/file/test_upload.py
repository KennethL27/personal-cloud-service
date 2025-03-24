import pytest
from tempfile import NamedTemporaryFile

class TestFileUpload:
    def test_file_upload(self, test_client):
        mock_file = NamedTemporaryFile(suffix='.jpeg')
        response = test_client.post("/file/upload", files = {"files": mock_file})

        assert response.json() == {"uploaded_files": [mock_file.name.rsplit('/',1)[1]]}

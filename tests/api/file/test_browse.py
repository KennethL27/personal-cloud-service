from unittest.mock import patch, MagicMock

class TestFileBrowse:
    def test_browse_all_files(self, test_client):
        with patch("src.api.file.browse.get_external_drive_path", return_value="/fake_drive/"), \
             patch("src.api.file.browse.os.path.exists", return_value=True), \
             patch("src.api.file.browse.os.listdir") as mock_listdir, \
             patch("src.api.file.browse.os.stat") as mock_stat, \
             patch("src.api.file.browse.mimetypes.guess_type", return_value=("image/jpeg", None)):
            
            # Mock file listing
            mock_listdir.side_effect = [
                ["photo1.jpg", "photo2.png"],  # photos folder
                ["video1.mp4"],  # videos folder
                ["doc1.pdf"],  # documents folder
                [],  # audio folder (empty)
                [],  # zip folder (empty)
                ["other.txt"]  # others folder
            ]
            
            # Mock file stats
            mock_stat.return_value = MagicMock(st_size=1024, st_mtime=1640995200)  # 2022-01-01
            
            response = test_client.get("/file/browse/")
            assert response.status_code == 200
            
            data = response.json()
            assert "files" in data
            assert "total_count" in data
            assert data["total_count"] == 5  # 2 photos + 1 video + 1 doc + 1 other
            
            # Check that files have required fields
            for file_info in data["files"]:
                assert "name" in file_info
                assert "size" in file_info
                assert "type" in file_info
                assert "modified" in file_info
                assert "category" in file_info

    def test_browse_by_category(self, test_client):
        with patch("src.api.file.browse.get_external_drive_path", return_value="/fake_drive/"), \
             patch("src.api.file.browse.os.path.exists", return_value=True), \
             patch("src.api.file.browse.os.listdir", return_value=["photo1.jpg", "photo2.png"]), \
             patch("src.api.file.browse.os.stat") as mock_stat, \
             patch("src.api.file.browse.mimetypes.guess_type", return_value=("image/jpeg", None)):
            
            mock_stat.return_value = MagicMock(st_size=1024, st_mtime=1640995200)
            
            response = test_client.get("/file/browse/?category=photos")
            assert response.status_code == 200
            
            data = response.json()
            assert data["total_count"] == 2
            
            # All files should be from photos category
            for file_info in data["files"]:
                assert file_info["category"] == "photos"

    def test_browse_invalid_category(self, test_client):
        with patch("src.api.file.browse.get_external_drive_path", return_value="/fake_drive/"):
            response = test_client.get("/file/browse/?category=invalid")
            assert response.status_code == 200
            
            data = response.json()
            assert data["total_count"] == 0
            assert data["files"] == []

    def test_browse_empty_directory(self, test_client):
        with patch("src.api.file.browse.get_external_drive_path", return_value="/fake_drive/"), \
             patch("src.api.file.browse.os.path.exists", return_value=True), \
             patch("src.api.file.browse.os.listdir", return_value=[]):
            
            response = test_client.get("/file/browse/?category=photos")
            assert response.status_code == 200
            
            data = response.json()
            assert data["total_count"] == 0
            assert data["files"] == []

    def test_browse_nonexistent_drive(self, test_client):
        with patch("src.api.file.browse.get_external_drive_path", return_value=None):
            response = test_client.get("/file/browse/")
            assert response.status_code == 200
            
            data = response.json()
            assert data["total_count"] == 0
            assert data["files"] == []

    def test_browse_nonexistent_folder(self, test_client):
        with patch("src.api.file.browse.get_external_drive_path", return_value="/fake_drive/"), \
             patch("src.api.file.browse.os.path.exists", return_value=False):
            
            response = test_client.get("/file/browse/?category=photos")
            assert response.status_code == 200
            
            data = response.json()
            assert data["total_count"] == 0
            assert data["files"] == []

    def test_browse_file_access_error(self, test_client):
        with patch("src.api.file.browse.get_external_drive_path", return_value="/fake_drive/"), \
             patch("src.api.file.browse.os.path.exists", return_value=True), \
             patch("src.api.file.browse.os.listdir", return_value=["photo1.jpg"]), \
             patch("src.api.file.browse.os.stat", side_effect=OSError("Permission denied")):
            
            response = test_client.get("/file/browse/?category=photos")
            assert response.status_code == 200
            
            data = response.json()
            assert data["total_count"] == 0
            assert data["files"] == []

    def test_browse_filters_hidden_files(self, test_client):
        with patch("src.api.file.browse.get_external_drive_path", return_value="/fake_drive/"), \
             patch("src.api.file.browse.os.path.exists", return_value=True), \
             patch("src.api.file.browse.os.listdir", return_value=["photo1.jpg", "._photo1.jpg", ".hidden.txt", "normal.txt"]), \
             patch("src.api.file.browse.os.stat") as mock_stat, \
             patch("src.api.file.browse.mimetypes.guess_type", return_value=("text/plain", None)):
            
            mock_stat.return_value = MagicMock(st_size=1024, st_mtime=1640995200)
            
            response = test_client.get("/file/browse/?category=others")
            assert response.status_code == 200
            
            data = response.json()
            assert data["total_count"] == 2  # Only photo1.jpg and normal.txt
            
            # Check that hidden files are filtered out
            file_names = [file_info["name"] for file_info in data["files"]]
            assert "photo1.jpg" in file_names
            assert "normal.txt" in file_names
            assert "._photo1.jpg" not in file_names
            assert ".hidden.txt" not in file_names

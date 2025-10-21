from unittest.mock import patch, MagicMock
import pytest
from pathlib import Path
from datetime import datetime

class TestListFolderItems:
    def mock_resolve_method(self):
        return Path("/test/drive")   
    
    def mock_truediv_method(self, other):
        # Use os.path.join to avoid recursion since __truediv__ is mocked
        import os.path
        return Path(os.path.join("/test/drive", str(other)))

    def test_list_folder_items_root_directory(self, test_client, bypass_auth):
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/test/drive"
        
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch("src.api.file.list_folder_items.get_user_by_email", return_value=mock_user), \
            patch("src.api.file.list_folder_items.get_user_setting", return_value=mock_user_setting), \
            patch("src.api.file.list_folder_items.Path.exists", return_value=True), \
            patch("src.api.file.list_folder_items.Path.is_dir", return_value=True), \
            patch("src.api.file.list_folder_items.Path.resolve") as mock_resolve, \
            patch("src.api.file.list_folder_items.Path.__truediv__") as mock_truediv, \
            patch("src.api.file.list_folder_items.Path.iterdir") as mock_iterdir, \
            patch("src.services.api.file.file_helper.is_hidden", return_value=False):

            mock_resolve.side_effect = self.mock_resolve_method
            mock_truediv.side_effect = self.mock_truediv_method
            
            # Mock directory contents
            mock_file1 = MagicMock()
            mock_file1.name = "document.pdf"
            mock_file1.is_dir.return_value = False
            mock_file1.is_file.return_value = True
            mock_file1.resolve.return_value = Path("/test/drive/document.pdf")
            mock_file1.relative_to.return_value = Path("document.pdf")

            mock_file2 = MagicMock()
            mock_file2.name = "photos"
            mock_file2.is_dir.return_value = True
            mock_file2.is_file.return_value = False
            mock_file2.resolve.return_value = Path("/test/drive/photos")
            mock_file2.relative_to.return_value = Path("photos")

            mock_iterdir.return_value = [mock_file1, mock_file2]

            # Mock file stats
            mock_stat1 = MagicMock()
            mock_stat1.st_size = 1024 * 1024  # 1MB
            mock_stat1.st_mtime = datetime(2023, 1, 15, 10, 30).timestamp()

            mock_stat2 = MagicMock()
            mock_stat2.st_size = 0  # directories have size 0
            mock_stat2.st_mtime = datetime(2023, 1, 15, 10, 30).timestamp()

            mock_file1.stat.return_value = mock_stat1
            mock_file2.stat.return_value = mock_stat2
            
            response = test_client.get("/file/list_folder_items/")
            assert response.status_code == 200
            
            data = response.json()
            assert len(data) == 2
            
            # Check first file (document.pdf)
            assert data[0]["name"] == "document.pdf"
            assert data[0]["type"] == "file"
            assert data[0]["size"] == "1.00 MB"
            assert "modified" in data[0]
            assert "relative_path" in data[0]
            assert "full_path" in data[0]
            
            # Check second entry (photos folder)
            assert data[1]["name"] == "photos"
            assert data[1]["type"] == "folder"
            assert data[1]["size"] is None

    def test_list_folder_items_subdirectory(self, test_client, bypass_auth):
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/test/drive"
        
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch("src.api.file.list_folder_items.get_user_by_email", return_value=mock_user), \
            patch("src.api.file.list_folder_items.get_user_setting", return_value=mock_user_setting), \
            patch("src.api.file.list_folder_items.Path.exists", return_value=True), \
            patch("src.api.file.list_folder_items.Path.is_dir", return_value=True), \
            patch("src.api.file.list_folder_items.Path.resolve") as mock_resolve, \
            patch("src.api.file.list_folder_items.Path.__truediv__") as mock_truediv, \
            patch("src.api.file.list_folder_items.Path.iterdir") as mock_iterdir, \
            patch("src.services.api.file.file_helper.is_hidden", return_value=False):

            mock_resolve.side_effect = self.mock_resolve_method
            mock_truediv.side_effect = self.mock_truediv_method
            
            # Mock single file in subdirectory
            mock_file = MagicMock()
            mock_file.name = "image.jpg"
            mock_file.is_dir.return_value = False
            mock_file.is_file.return_value = True
            mock_file.resolve.return_value = Path("/test/drive/photos/image.jpg")
            mock_file.relative_to.return_value = Path("photos/image.jpg")
            
            mock_iterdir.return_value = [mock_file]
            
            # Mock file stats
            mock_stat = MagicMock()
            mock_stat.st_size = 2048
            mock_stat.st_mtime = datetime(2023, 1, 15, 10, 30).timestamp()
            
            mock_file.stat.return_value = mock_stat

    def test_list_folder_items_filters_hidden_files(self, test_client, bypass_auth):
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/test/drive"
        
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch("src.api.file.list_folder_items.get_user_by_email", return_value=mock_user), \
             patch("src.api.file.list_folder_items.get_user_setting", return_value=mock_user_setting), \
             patch("src.api.file.list_folder_items.Path.exists", return_value=True), \
             patch("src.api.file.list_folder_items.Path.is_dir", return_value=True), \
             patch("src.api.file.list_folder_items.Path.resolve") as mock_resolve, \
             patch("src.api.file.list_folder_items.Path.__truediv__") as mock_truediv, \
             patch("src.api.file.list_folder_items.Path.iterdir") as mock_iterdir, \
             patch("src.api.file.list_folder_items.Path.stat") as mock_stat:
            
            mock_resolve.side_effect = self.mock_resolve_method
            mock_truediv.side_effect = self.mock_truediv_method
            
            # Mock files where some are hidden
            mock_normal_file = MagicMock()
            mock_normal_file.name = "normal.txt"
            mock_normal_file.is_dir.return_value = False
            mock_normal_file.is_file.return_value = True
            mock_normal_file.resolve.return_value = Path("/test/drive/normal.txt")
            mock_normal_file.relative_to.return_value = Path("normal.txt")
            
            mock_hidden_file = MagicMock()
            mock_hidden_file.name = ".hidden.txt"
            mock_hidden_file.is_dir.return_value = False
            mock_hidden_file.is_file.return_value = True
            mock_hidden_file.resolve.return_value = Path("/test/drive/.hidden.txt")
            mock_hidden_file.relative_to.return_value = Path(".hidden.txt")
            
            mock_iterdir.return_value = [mock_normal_file, mock_hidden_file]
            
            # Mock file stats
            mock_stat_normal = MagicMock()
            mock_stat_normal.st_size = 1024
            mock_stat_normal.st_mtime = datetime(2023, 1, 15, 10, 30).timestamp()
            
            mock_stat_hidden = MagicMock()
            mock_stat_hidden.st_size = 512
            mock_stat_hidden.st_mtime = datetime(2023, 1, 15, 10, 30).timestamp()
            
            mock_normal_file.stat.return_value = mock_stat_normal
            mock_hidden_file.stat.return_value = mock_stat_hidden
            
            def is_hidden_side_effect(path):
                return path.name.startswith('.')
            
            with patch("src.services.api.file.file_helper.is_hidden", side_effect=is_hidden_side_effect):
                response = test_client.get("/file/list_folder_items")
                assert response.status_code == 200
                
                data = response.json()
                assert len(data) == 1
                assert data[0]["name"] == "normal.txt"

    def test_list_folder_items_directory_not_found(self, test_client, bypass_auth):
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/test/drive"
        
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch("src.api.file.list_folder_items.get_user_by_email", return_value=mock_user), \
             patch("src.api.file.list_folder_items.get_user_setting", return_value=mock_user_setting), \
             patch("src.api.file.list_folder_items.Path.exists", return_value=False), \
             patch("src.api.file.list_folder_items.Path.resolve") as mock_resolve, \
             patch("src.api.file.list_folder_items.Path.__truediv__") as mock_truediv:
            
            mock_resolve.side_effect = self.mock_resolve_method
            mock_truediv.side_effect = self.mock_truediv_method
            
            response = test_client.get("/file/list_folder_items/?path=nonexistent")
            assert response.status_code == 404

    def test_list_folder_items_path_is_file(self, test_client, bypass_auth):
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/test/drive"
        
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch("src.api.file.list_folder_items.get_user_by_email", return_value=mock_user), \
             patch("src.api.file.list_folder_items.get_user_setting", return_value=mock_user_setting), \
             patch("src.api.file.list_folder_items.Path.exists", return_value=True), \
             patch("src.api.file.list_folder_items.Path.is_dir", return_value=False), \
             patch("src.api.file.list_folder_items.Path.resolve") as mock_resolve, \
             patch("src.api.file.list_folder_items.Path.__truediv__") as mock_truediv:
            
            mock_resolve.side_effect = self.mock_resolve_method
            mock_truediv.side_effect = self.mock_truediv_method
            
            response = test_client.get("/file/list_folder_items/?path=file_not_directory")
            assert response.status_code == 400

    def test_list_folder_items_directory_traversal_attack(self, test_client, bypass_auth):
        """Test prevention of directory traversal attacks."""
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/test/drive"
        
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch("src.api.file.list_folder_items.get_user_by_email", return_value=mock_user), \
             patch("src.api.file.list_folder_items.get_user_setting", return_value=mock_user_setting), \
             patch("src.api.file.list_folder_items.Path.resolve") as mock_resolve, \
             patch("src.api.file.list_folder_items.Path.__truediv__") as mock_truediv:
            
            mock_resolve.side_effect = self.mock_resolve_method
            mock_truediv.side_effect = self.mock_truediv_method
            
            # This would try to access a path outside the base directory
            response = test_client.get("/file/list_folder_items/?path=../../../etc")
            assert response.status_code == 404

    def test_list_folder_items_permission_denied(self, test_client, bypass_auth):
        """Test handling of permission errors."""
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/test/drive"
        
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch("src.api.file.list_folder_items.get_user_by_email", return_value=mock_user), \
             patch("src.api.file.list_folder_items.get_user_setting", return_value=mock_user_setting), \
             patch("src.api.file.list_folder_items.Path.exists", return_value=True), \
             patch("src.api.file.list_folder_items.Path.is_dir", return_value=True), \
             patch("src.api.file.list_folder_items.Path.resolve") as mock_resolve, \
             patch("src.api.file.list_folder_items.Path.__truediv__") as mock_truediv, \
             patch("src.api.file.list_folder_items.Path.iterdir", side_effect=PermissionError("Permission denied")):
            
            mock_resolve.side_effect = self.mock_resolve_method
            mock_truediv.side_effect = self.mock_truediv_method
            
            response = test_client.get("/file/list_folder_items")
            assert response.status_code == 403

    def test_list_folder_items_empty_directory(self, test_client, bypass_auth):
        """Test listing an empty directory."""
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/test/drive"
        
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch("src.api.file.list_folder_items.get_user_by_email", return_value=mock_user), \
             patch("src.api.file.list_folder_items.get_user_setting", return_value=mock_user_setting), \
             patch("src.api.file.list_folder_items.Path.exists", return_value=True), \
             patch("src.api.file.list_folder_items.Path.is_dir", return_value=True), \
             patch("src.api.file.list_folder_items.Path.resolve") as mock_resolve, \
             patch("src.api.file.list_folder_items.Path.__truediv__") as mock_truediv, \
             patch("src.api.file.list_folder_items.Path.iterdir", return_value=[]), \
             patch("src.services.api.file.file_helper.is_hidden", return_value=False):
            
            mock_resolve.side_effect = self.mock_resolve_method
            mock_truediv.side_effect = self.mock_truediv_method
            
            response = test_client.get("/file/list_folder_items")
            assert response.status_code == 200
            
            data = response.json()
            assert data == []

    def test_list_folder_items_general_exception(self, test_client, bypass_auth):
        """Test handling of general exceptions."""
        mock_user_setting = MagicMock()
        mock_user_setting.hard_drive_path_selection = "/test/drive"
        
        mock_user = MagicMock()
        mock_user.id = 1
        
        with patch("src.api.file.list_folder_items.get_user_by_email", return_value=mock_user), \
             patch("src.api.file.list_folder_items.get_user_setting", return_value=mock_user_setting), \
             patch("src.api.file.list_folder_items.Path.exists", return_value=True), \
             patch("src.api.file.list_folder_items.Path.is_dir", return_value=True), \
             patch("src.api.file.list_folder_items.Path.resolve") as mock_resolve, \
             patch("src.api.file.list_folder_items.Path.__truediv__") as mock_truediv, \
             patch("src.api.file.list_folder_items.Path.iterdir", side_effect=Exception("Unexpected error")):
            
            mock_resolve.side_effect = self.mock_resolve_method
            mock_truediv.side_effect = self.mock_truediv_method
            
            response = test_client.get("/file/list_folder_items")
            assert response.status_code == 500

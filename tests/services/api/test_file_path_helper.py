from src.services.api.file_path_helper import *
from unittest.mock import patch, Mock

class TestFilePathHelper:
    def test_get_external_drive_path__darwin(self):
        with patch("src.services.api.file_path_helper.platform.system", return_value="Darwin"), \
             patch("src.services.api.file_path_helper.os.listdir", return_value=["Drive1", "Drive2"]), \
             patch("src.services.api.file_path_helper.os.path.isdir", return_value=True):
            assert get_external_drive_path() == "/Volumes/Drive2"

    def test_get_external_drive_path__linux(self):
        with patch("src.services.api.file_path_helper.platform.system", return_value="Linux"), \
             patch("src.services.api.file_path_helper.os.listdir", return_value=["Drive1", "Drive2"]), \
             patch("src.services.api.file_path_helper.os.path.isdir", return_value=True):
            assert get_external_drive_path() == "/media/pi/Drive2"
            
    def test_get_external_drive_path__windows(self):
        mock_partition = Mock()
        mock_partition.mountpoint = "D:\\"
        mock_partition.opts = "removable"
        with patch("src.services.api.file_path_helper.platform.system", return_value="Windows"), \
             patch("src.services.api.file_path_helper.psutil.disk_partitions", return_value=[mock_partition]):
            assert get_external_drive_path() == "D:\\"

        with patch("src.services.api.file_path_helper.platform.system", return_value="Windows"), \
             patch("src.services.api.file_path_helper.psutil.disk_partitions", return_value=[]):
            assert get_external_drive_path() is None
            
    def test_get_external_drive_path__unsupported_os(self):
        with patch("src.services.api.file_path_helper.platform.system", return_value="UnsupportedOS"):
            try:
                get_external_drive_path()
            except RuntimeError as e:
                assert str(e) == "Unsupported OS"

    def test_get_folder_destination(self):
        photo_file_type = "jpeg"
        expected_destination = "/photos"
        assert get_folder_destination(photo_file_type) == expected_destination
        
        video_file_type = "video/mp4"
        expected_video_destination = "/videos"
        assert get_folder_destination(video_file_type) == expected_video_destination

        audio_file_type = "audio/mpeg"
        expected_audio_destination = "/audio"
        assert get_folder_destination(audio_file_type) == expected_audio_destination
        
        document_file_type = "application/pdf"
        expected_document_destination = "/documents"
        assert get_folder_destination(document_file_type) == expected_document_destination
        
        zip_file_type = "application/zip"
        expected_zip_destination = "/zip"
        assert get_folder_destination(zip_file_type) == expected_zip_destination
        
        other_file_type = "text/plain"
        expected_other_destination = "/others"
        assert get_folder_destination(other_file_type) == expected_other_destination
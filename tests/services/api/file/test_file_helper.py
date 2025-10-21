import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.services.api.file.file_helper import bytes_to_human_readable, is_hidden

class TestBytesToHumanReadable:
    def test_bytes_to_human_readable_bytes(self):
        assert bytes_to_human_readable(512) == "512.00 B"
        assert bytes_to_human_readable(0) == "0.00 B"
        assert bytes_to_human_readable(1023) == "1023.00 B"

    def test_bytes_to_human_readable_kilobytes(self):
        assert bytes_to_human_readable(1024) == "1.00 KB"
        assert bytes_to_human_readable(1536) == "1.50 KB"
        assert bytes_to_human_readable(1024 * 1023) == "1023.00 KB"

    def test_bytes_to_human_readable_megabytes(self):
        assert bytes_to_human_readable(1024 * 1024) == "1.00 MB"
        assert bytes_to_human_readable(1024 * 1024 * 1.5) == "1.50 MB"
        assert bytes_to_human_readable(1024 * 1024 * 1023) == "1023.00 MB"

    def test_bytes_to_human_readable_gigabytes(self):
        assert bytes_to_human_readable(1024 * 1024 * 1024) == "1.00 GB"
        assert bytes_to_human_readable(1024 * 1024 * 1024 * 2.5) == "2.50 GB"
        assert bytes_to_human_readable(1024 * 1024 * 1024 * 1023) == "1023.00 GB"

    def test_bytes_to_human_readable_terabytes(self):
        assert bytes_to_human_readable(1024 * 1024 * 1024 * 1024) == "1.00 TB"
        assert bytes_to_human_readable(1024 * 1024 * 1024 * 1024 * 1.7) == "1.70 TB"
        assert bytes_to_human_readable(1024 * 1024 * 1024 * 1024 * 1023) == "1023.00 TB"

    def test_bytes_to_human_readable_petabytes(self):
        assert bytes_to_human_readable(1024 * 1024 * 1024 * 1024 * 1024) == "1.00 PB"
        assert bytes_to_human_readable(1024 * 1024 * 1024 * 1024 * 1024 * 2) == "2.00 PB"

    def test_bytes_to_human_readable_negative_value_error(self):
        with pytest.raises(ValueError, match="num_bytes must be a non-negative number"):
            bytes_to_human_readable(-1024)

class TestIsHidden:
    def test_is_hidden__unix__dot_file(self):
        path = Path("/test/.hidden_file.txt")
        assert is_hidden(path) == True

    def test_is_hidden__unix__dot_folder(self):
        path = Path("/test/.hidden_folder")
        assert is_hidden(path) == True

    def test_is_hidden__unix__normal_file(self):
        path = Path("/test/normal_file.txt")
        assert is_hidden(path) == False

    def test_is_hidden__unix__normal_folder(self):
        path = Path("/test/normal_folder")
        assert is_hidden(path) == False

    def test_windows_hidden_attribute_set(self):
        path = Path('hidden_file.txt')
        mock_windll = MagicMock()
        mock_windll.kernel32.GetFileAttributesW.return_value = 2  # FILE_ATTRIBUTE_HIDDEN
        
        with patch('src.services.api.file.file_helper.os.name', 'nt'):
            with patch('src.services.api.file.file_helper.ctypes.windll', mock_windll, create=True):
                assert is_hidden(path) == True

    def test_windows_normal_file_not_hidden(self):
        path = Path('normal_file.txt')
        mock_windll = MagicMock()
        mock_windll.kernel32.GetFileAttributesW.return_value = 0  # No hidden attribute
        
        with patch('src.services.api.file.file_helper.os.name', 'nt'):
            with patch('src.services.api.file.file_helper.ctypes.windll', mock_windll, create=True):
                assert is_hidden(path) == False

    def test_windows_error_handling_returns_false(self):
        path = Path('file.txt')
        mock_windll = MagicMock()
        mock_windll.kernel32.GetFileAttributesW.return_value = -1  # Error case
        
        with patch('src.services.api.file.file_helper.os.name', 'nt'):
            with patch('src.services.api.file.file_helper.ctypes.windll', mock_windll, create=True):
                assert is_hidden(path) == False

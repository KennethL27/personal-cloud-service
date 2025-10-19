import pytest
from src.services.api.file.file_helper import bytes_to_human_readable

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

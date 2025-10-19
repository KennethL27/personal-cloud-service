from unittest.mock import patch, MagicMock

class TestListMountedDrives:
    def test_list_mounted_drives_success(self, test_client, bypass_auth):
        # Mock partition data
        mock_partition1 = MagicMock()
        mock_partition1.device = "/dev/sda1"
        mock_partition1.mountpoint = "/mnt/drive1"
        mock_partition1.fstype = "ext4"
        mock_partition1.opts = "rw,relatime"
        
        mock_partition2 = MagicMock()
        mock_partition2.device = "/dev/sdb1"
        mock_partition2.mountpoint = "/mnt/drive2"
        mock_partition2.fstype = "ntfs"
        mock_partition2.opts = "rw,nosuid,nodev"
        
        # Mock usage data
        mock_usage1 = MagicMock()
        mock_usage1.total = 1000000000  # 1GB
        mock_usage1.used = 500000000   # 500MB
        mock_usage1.free = 500000000   # 500MB
        mock_usage1.percent = 50.0
        
        mock_usage2 = MagicMock()
        mock_usage2.total = 2000000000  # 2GB
        mock_usage2.used = 1000000000  # 1GB
        mock_usage2.free = 1000000000  # 1GB
        mock_usage2.percent = 50.0
        
        with patch("src.api.file.list_mounted_drives.psutil.disk_partitions", return_value=[mock_partition1, mock_partition2]), \
             patch("src.api.file.list_mounted_drives.psutil.disk_usage") as mock_disk_usage, \
             patch("src.api.file.list_mounted_drives.bytes_to_human_readable") as mock_bytes_to_human:
            
            # Configure mock return values
            mock_disk_usage.side_effect = [mock_usage1, mock_usage2]
            mock_bytes_to_human.side_effect = [
                "1.00 GB", "500.00 MB", "500.00 MB",
                "2.00 GB", "1.00 GB", "1.00 GB" 
            ] 
            
            response = test_client.get("/file/list_mounted_drives/")
            assert response.status_code == 200
            
            data = response.json()
            assert len(data) == 2
            
            # Check first drive data
            drive1 = next(d for d in data if d["device"] == "/dev/sda1")
            assert drive1["mountpoint"] == "/mnt/drive1"
            assert drive1["fstype"] == "ext4"
            assert drive1["opts"] == "rw,relatime"
            assert drive1["total"] == "1.00 GB"
            assert drive1["used"] == "500.00 MB"
            assert drive1["free"] == "500.00 MB"
            assert drive1["percent_used"] == "50.0%"
            
            # Check second drive data
            drive2 = next(d for d in data if d["device"] == "/dev/sdb1")
            assert drive2["mountpoint"] == "/mnt/drive2"
            assert drive2["fstype"] == "ntfs"
            assert drive2["opts"] == "rw,nosuid,nodev"
            assert drive2["total"] == "2.00 GB"
            assert drive2["used"] == "1.00 GB"
            assert drive2["free"] == "1.00 GB"
            assert drive2["percent_used"] == "50.0%"

    def test_list_mounted_drives_filters_apfs(self, test_client, bypass_auth):
        mock_partition_apfs = MagicMock()
        mock_partition_apfs.device = "/dev/disk1s1"
        mock_partition_apfs.mountpoint = "/System/Volumes/VM"
        mock_partition_apfs.fstype = "apfs"
        mock_partition_apfs.opts = "ro"
        
        mock_partition_ext4 = MagicMock()
        mock_partition_ext4.device = "/dev/sda1"
        mock_partition_ext4.mountpoint = "/mnt/drive1"
        mock_partition_ext4.fstype = "ext4"
        mock_partition_ext4.opts = "rw"
        
        mock_usage = MagicMock()
        mock_usage.total = 1000000000
        mock_usage.used = 500000000
        mock_usage.free = 500000000
        mock_usage.percent = 50.0
        
        with patch("src.api.file.list_mounted_drives.psutil.disk_partitions", return_value=[mock_partition_apfs, mock_partition_ext4]), \
             patch("src.api.file.list_mounted_drives.psutil.disk_usage", return_value=mock_usage), \
             patch("src.api.file.list_mounted_drives.bytes_to_human_readable") as mock_bytes_to_human:
            
            mock_bytes_to_human.side_effect = ["1.00 GB", "500.00 MB", "500.00 MB"]
            
            response = test_client.get("/file/list_mounted_drives/")
            assert response.status_code == 200
            
            data = response.json()
            assert len(data) == 1
            assert data[0]["fstype"] == "ext4"
            assert data[0]["device"] == "/dev/sda1"
            assert data[0]["total"] == "1.00 GB"
            assert data[0]["used"] == "500.00 MB"
            assert data[0]["free"] == "500.00 MB"
            assert data[0]["percent_used"] == "50.0%"

    def test_list_mounted_drives_handles_permission_error(self, test_client, bypass_auth):
        mock_partition = MagicMock()
        mock_partition.device = "/dev/sda1"
        mock_partition.mountpoint = "/mnt/restricted"
        mock_partition.fstype = "ext4"
        mock_partition.opts = "rw"
        
        with patch("src.api.file.list_mounted_drives.psutil.disk_partitions", return_value=[mock_partition]), \
             patch("src.api.file.list_mounted_drives.psutil.disk_usage", side_effect=PermissionError("Permission denied")):
            
            response = test_client.get("/file/list_mounted_drives/")
            assert response.status_code == 200
            
            data = response.json()
            # Should return empty list when permission denied
            assert data == []

    def test_list_mounted_drives_handles_generic_exception(self, test_client, bypass_auth):
        mock_partition = MagicMock()
        mock_partition.device = "/dev/sda1"
        mock_partition.mountpoint = "/mnt/drive1"
        mock_partition.fstype = "ext4"
        mock_partition.opts = "rw"
        
        with patch("src.api.file.list_mounted_drives.psutil.disk_partitions", return_value=[mock_partition]), \
             patch("src.api.file.list_mounted_drives.psutil.disk_usage", side_effect=Exception("Some error")):
            
            response = test_client.get("/file/list_mounted_drives/")
            assert response.status_code == 200
            
            data = response.json()
            # Should return empty list when generic error occurs
            assert data == []

    def test_list_mounted_drives_empty_partitions(self, test_client, bypass_auth):
        with patch("src.api.file.list_mounted_drives.psutil.disk_partitions", return_value=[]):
            response = test_client.get("/file/list_mounted_drives/")
            assert response.status_code == 200
            
            data = response.json()
            assert data == []

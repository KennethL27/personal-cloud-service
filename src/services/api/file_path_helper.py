import platform
import os
try:
    import psutil
except ImportError:
    psutil = None

def get_external_drive_path():
    system = platform.system()

    if system == "Darwin":  # macOS
        base_path = "/Volumes"
    elif system == "Linux":
        base_path = "/media/pi"  # Adjust based on your user/mount path on RPi
    elif system == "Windows":
        base_path = None  # Windows uses drive letters
    else:
        raise RuntimeError("Unsupported OS")

    if system in ["Darwin", "Linux"]:
        # Find mounted drives
        drives = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        return os.path.join(base_path, drives[1]) if len(drives) > 1 else None
    else:  # Windows
        if psutil is None:
            raise ImportError("psutil is required for Windows support")
        for partition in psutil.disk_partitions():
            if "removable" in partition.opts.lower():  # Detect USB drive
                return partition.mountpoint

    return None

def get_folder_destination(file_type):
    if file_type in ['image/jpeg', 'jpeg', 'jpg']:
        return "/photos"
    elif file_type in ['video/mp4', 'video/quicktime', 'mp4', 'mov']:
        return "/videos"
    elif file_type in ['audio/mpeg', 'mpeg']:
        return "/audio"
    elif file_type in ['application/pdf', 'pdf']:
        return "/documents"
    elif file_type in ['application/zip', 'zip']:
        return "/zip"
    else:
        return "/others"
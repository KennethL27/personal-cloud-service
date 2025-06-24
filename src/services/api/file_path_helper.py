import platform
import os

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
        return os.path.join(base_path, drives[1]) if drives else None
    else:  # Windows
        import psutil
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
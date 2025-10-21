# api/file/file_helper.py
from pathlib import Path
import ctypes
import os

def bytes_to_human_readable(num_bytes: float) -> str:
    if num_bytes < 0:
        raise ValueError("num_bytes must be a non-negative number")

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    for unit in units:
        if num_bytes < 1024.0:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.2f} {units[-1]}"

def is_hidden(path: Path) -> bool:
    """Check if file/folder is hidden on Linux/macOS/Windows."""
    if path.name.startswith('.'):
        return True
    if os.name == 'nt':  # Windows hidden attribute check
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
        return attrs != -1 and (attrs & 2) != 0  # FILE_ATTRIBUTE_HIDDEN = 0x2
    return False
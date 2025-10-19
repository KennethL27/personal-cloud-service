# api/file/file_helper.py

def bytes_to_human_readable(num_bytes: float) -> str:
    if num_bytes < 0:
        raise ValueError("num_bytes must be a non-negative number")

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    for unit in units:
        if num_bytes < 1024.0:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.2f} {units[-1]}"
from fastapi import APIRouter
from pydantic import BaseModel, Field
from src.services.api.file.file_helper import bytes_to_human_readable
import psutil

router = APIRouter(tags=["File"])

class DriveInfo(BaseModel):
    device: str = Field(..., description="Device path", example="/drive_1")
    mountpoint: str = Field(..., description="Mount point path", example="/Volumes/disk_1")
    fstype: str = Field(..., description="Filesystem type", example="msdos")
    opts: str = Field(..., description="Mount options", example="rw,nosuid,local,ignore-ownership,noatime")
    total: str = Field(..., description="Total capacity", example="999.9 MB")
    used: str = Field(..., description="Used space", example="555.5 MB")
    free: str = Field(..., description="Free space", example="999.9 MB")
    percent_used: str = Field(..., description="Percentage used", example="50.5%")

@router.get('/', response_model=list[DriveInfo])
async def list_mounted_drives():
    """List all drives attached to the server"""
    drives_info = []
    partitions = psutil.disk_partitions(all=False)  

    for partition in partitions:
        if partition.fstype == 'apfs':
                continue

        try:
            usage = psutil.disk_usage(partition.mountpoint)
            drive_data = {
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "opts": partition.opts,
                "total": bytes_to_human_readable(usage.total),
                "used": bytes_to_human_readable(usage.used),
                "free": bytes_to_human_readable(usage.free),
                "percent_used": f"{usage.percent}%",
            }
            drives_info.append(drive_data)
        except PermissionError:
            # Skip partitions the process doesn’t have access to
            continue
        except Exception:
            # Handle transient or non-standard partitions gracefully
            continue

    return drives_info

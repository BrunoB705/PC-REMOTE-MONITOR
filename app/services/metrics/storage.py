import psutil

DRIVES = ["C:\\", "D:\\", "E:\\"]

def get_all_storage():
    result = {}
    for drive in DRIVES:
        try:
            disk = psutil.disk_usage(drive)
            result[drive] = {
                "used": round(disk.used / (1024 ** 3), 1),
                "total": round(disk.total / (1024 ** 3), 1),
                "percentage": disk.percent
            }
        except Exception:
            result[drive] = None
    return result
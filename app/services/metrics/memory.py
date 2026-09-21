import psutil

def get_memory():
    try:
        mem = psutil.virtual_memory()
        return {
            "used": round(mem.used / (1024 ** 3), 1),
            "total": round(mem.total / (1024 ** 3), 1),
            "percentage": mem.percent
        }
    except Exception:
        pass
    return None

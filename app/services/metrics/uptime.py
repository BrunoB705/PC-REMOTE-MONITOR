import psutil
import time

def get_uptime():
    return int(time.time() - psutil.boot_time())
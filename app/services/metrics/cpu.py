import psutil

def get_cpu_usage():
    try:
        return psutil.cpu_percent(interval=None)
    except Exception:
        pass
    return None

def get_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            return temps["coretemp"][0].current
    except Exception:
        pass
    return None

def get_cpu_frequency():
    try:
        freqs = psutil.cpu_freq()
        if freqs:
            return freqs.current
    except Exception:
        pass
    return None

def get_cpu_fan_speed():
    try:
        return psutil.cpu_fan_speed().current
    except Exception:
        pass
    return None
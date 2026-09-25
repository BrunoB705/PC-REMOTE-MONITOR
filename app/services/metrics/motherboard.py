from app.services.metrics import manager


def get_motherboard_temperature():
    try:
        from LibreHardwareMonitor.Hardware import HardwareType, SensorType
        computer = manager.refresh()
        if computer is None:
            return None
        fallback = None
        for hardware in computer.Hardware:
            if hardware.HardwareType != HardwareType.Motherboard:
                continue
            for sensor in manager.iter_sensors(hardware):
                if sensor.SensorType != SensorType.Temperature or sensor.Value is None:
                    continue
                value = float(sensor.Value)
                if value <= 0:
                    continue
                if "System" in sensor.Name:
                    return value
                if fallback is None:
                    fallback = value
            return fallback
        return None
    except Exception:
        pass
    return None

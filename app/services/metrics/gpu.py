from app.services.metrics import manager


def get_gpu():
    try:
        from LibreHardwareMonitor.Hardware import HardwareType, SensorType
        computer = manager.refresh()
        if computer is None:
            return None
        gpu_types = (HardwareType.GpuAmd, HardwareType.GpuNvidia, HardwareType.GpuIntel)
        best = None
        best_memory = -1.0
        for hardware in computer.Hardware:
            if hardware.HardwareType not in gpu_types:
                continue
            info = {
                "name": hardware.Name,
                "temperature": None,
                "usage": None,
                "vram_used": None,
                "vram_total": None,
            }
            memory_total = 0.0
            for sensor in manager.iter_sensors(hardware):
                if sensor.Value is None:
                    continue
                name = sensor.Name
                stype = sensor.SensorType
                if stype == SensorType.Temperature and name == "GPU Core":
                    info["temperature"] = float(sensor.Value)
                elif stype == SensorType.Load and name == "GPU Core":
                    info["usage"] = float(sensor.Value)
                elif stype == SensorType.SmallData and name == "GPU Memory Total":
                    memory_total = float(sensor.Value)
                    info["vram_total"] = round(memory_total / 1024, 1)
                elif stype == SensorType.SmallData and name == "GPU Memory Used":
                    info["vram_used"] = round(float(sensor.Value) / 1024, 1)
            if info["temperature"] is None and info["usage"] is None:
                continue
            if memory_total > best_memory:
                best = info
                best_memory = memory_total
        return best
    except Exception:
        pass
    return None

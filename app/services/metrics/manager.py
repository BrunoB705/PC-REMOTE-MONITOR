import logging
import os

logger = logging.getLogger(__name__)

DLL_PATH = os.path.join(os.path.dirname(__file__), "lib", "LibreHardwareMonitorLib.dll")

_computer = None
_available = False


def open_manager():
    global _computer, _available
    if _available:
        return True
    if not os.path.exists(DLL_PATH):
        logger.warning("DLL no encontrado: %s", DLL_PATH)
        return False
    try:
        try:
            import pythonnet
            pythonnet.load("netfx")
        except Exception:
            pass
        import clr
        clr.AddReference(DLL_PATH)
        from LibreHardwareMonitor.Hardware import Computer

        computer = Computer()
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.IsMotherboardEnabled = True
        computer.Open()

        _computer = computer
        _available = True
        logger.info("LibreHardwareMonitor abierto")
        return True
    except Exception:
        logger.exception("No se pudo abrir LibreHardwareMonitor (¿ejecutar como administrador?)")
        _computer = None
        _available = False
        return False


def close_manager():
    global _computer, _available
    if _computer is not None:
        try:
            _computer.Close()
        except Exception:
            logger.exception("Error al cerrar LibreHardwareMonitor")
    _computer = None
    _available = False


def is_available():
    return _available


def refresh():
    if not _available or _computer is None:
        return None
    try:
        for hardware in _computer.Hardware:
            hardware.Update()
            for sub in hardware.SubHardware:
                sub.Update()
        return _computer
    except Exception:
        logger.exception("Error al actualizar sensores")
        return None


def iter_sensors(hardware):
    for sensor in hardware.Sensors:
        yield sensor
    for sub in hardware.SubHardware:
        for sensor in sub.Sensors:
            yield sensor

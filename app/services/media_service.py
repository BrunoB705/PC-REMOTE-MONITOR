import ctypes
import logging

logger = logging.getLogger(__name__)

# VK de las teclas multimedia (nunca vienen del usuario)
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PLAY_PAUSE = 0xB3

INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002

ULONG_PTR = ctypes.c_size_t


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_uint),
        ("time", ctypes.c_uint),
        ("dwExtraInfo", ULONG_PTR),
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_uint),
        ("dwFlags", ctypes.c_uint),
        ("time", ctypes.c_uint),
        ("dwExtraInfo", ULONG_PTR),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_uint),
        ("wParamL", ctypes.c_ushort),
        ("wParamH", ctypes.c_ushort),
    ]


class _INPUTUNION(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
        ("mi", MOUSEINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_uint),
        ("u", _INPUTUNION),
    ]


user32 = ctypes.WinDLL("user32", use_last_error=True)
user32.SendInput.restype = ctypes.c_uint


def _key_input(vk: int, flags: int) -> INPUT:
    event = INPUT()
    event.type = INPUT_KEYBOARD
    event.u.ki.wVk = vk
    event.u.ki.dwFlags = flags
    return event


def _send_key(vk: int) -> bool:
    """Envía el par keydown/keyup de una VK; True solo si el SO aceptó los 2 eventos."""
    events = (INPUT * 2)(_key_input(vk, 0), _key_input(vk, KEYEVENTF_KEYUP))
    try:
        sent = user32.SendInput(2, events, ctypes.sizeof(INPUT))
    except (OSError, ValueError):
        logger.exception("SendInput lanzó una excepción para vk=0x%02X", vk)
        return False
    if sent != 2:
        logger.error("SendInput rechazó vk=0x%02X (envió %s de 2)", vk, sent)
        return False
    return True


def vol_up() -> bool:
    return _send_key(VK_VOLUME_UP)


def vol_down() -> bool:
    return _send_key(VK_VOLUME_DOWN)


def mute() -> bool:
    return _send_key(VK_VOLUME_MUTE)


def play_pause() -> bool:
    return _send_key(VK_MEDIA_PLAY_PAUSE)


def next_track() -> bool:
    return _send_key(VK_MEDIA_NEXT_TRACK)


def prev_track() -> bool:
    return _send_key(VK_MEDIA_PREV_TRACK)

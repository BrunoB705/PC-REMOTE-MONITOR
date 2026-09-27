import logging
import subprocess

logger = logging.getLogger(__name__)

# Segundos de gracia antes de apagar/reiniciar, para poder cancelar con shutdown /a
SHUTDOWN_DELAY = 30

# shutdown /a devuelve esto cuando no había nada programado (verificado en la PC real)
EXIT_NOT_SCHEDULED = 1116

# Apagar monitoreo (SC_MONITORPOWER, 2 = off) via user32.SendMessage
PS_MONITOR_OFF = (
    "Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; "
    "public class Mon { [DllImport(\"user32.dll\")] public static extern int SendMessage("
    "int hWnd, uint Msg, IntPtr wParam, IntPtr lParam); }'; "
    "[Mon]::SendMessage(0xFFFF, 0x0112, [IntPtr]0xF170, [IntPtr]2)"
)


def _execute(cmd: list[str]) -> int | None:
    """Devuelve el returncode, o None si no se pudo ejecutar."""
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            timeout=15,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except (OSError, subprocess.SubprocessError):
        logger.exception("No se pudo ejecutar: %s", cmd)
        return None
    if proc.returncode != 0:
        logger.error(
            "%s devolvió rc=%s: %s",
            cmd,
            proc.returncode,
            proc.stderr.decode("utf-8", errors="replace").strip(),
        )
    return proc.returncode


def _run(cmd: list[str]) -> bool:
    return _execute(cmd) == 0


def shutdown_pc() -> bool:
    return _run(["shutdown", "/s", "/t", str(SHUTDOWN_DELAY)])


def restart_pc() -> bool:
    return _run(["shutdown", "/r", "/t", str(SHUTDOWN_DELAY)])


def cancel_shutdown() -> bool | None:
    """True = canceló un apagado, False = no había nada programado, None = error."""
    rc = _execute(["shutdown", "/a"])
    if rc == EXIT_NOT_SCHEDULED:
        return False
    if rc == 0:
        return True
    return None


def sleep_pc() -> bool:
    return _run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])


def lock_pc() -> bool:
    return _run(["rundll32.exe", "user32.dll,LockWorkStation"])


def monitor_off() -> bool:
    return _run(["powershell", "-NoProfile", "-NonInteractive", "-Command", PS_MONITOR_OFF])

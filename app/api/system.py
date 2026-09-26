from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.security import require_api_key
from app.services import system_service

router = APIRouter(dependencies=[Depends(require_api_key)])

# action -> (función del servicio, mensaje al usuario)
ACTIONS: dict[str, tuple] = {
    "apagar": (system_service.shutdown_pc, f"Apagando la PC en {system_service.SHUTDOWN_DELAY} segundos"),
    "reiniciar": (system_service.restart_pc, f"Reiniciando la PC en {system_service.SHUTDOWN_DELAY} segundos"),
    "cancelar": (system_service.cancel_shutdown, "Apagado cancelado"),
    "suspender": (system_service.sleep_pc, "PC en suspensión"),
    "bloquear": (system_service.lock_pc, "PC bloqueada"),
    "apagar_pantalla": (system_service.monitor_off, "Pantalla apagada"),
}


class ConfirmPayload(BaseModel):
    confirm: bool = False


@router.post("/api/system/{action}")
def run_system_action(action: str, payload: ConfirmPayload | None = None):
    if action not in ACTIONS:
        raise HTTPException(status_code=404, detail="Acción desconocida")
    if payload is None or not payload.confirm:
        raise HTTPException(status_code=400, detail="Confirmación requerida")

    func, message = ACTIONS[action]
    if not func():
        raise HTTPException(status_code=500, detail="No se pudo ejecutar la acción")

    response = {"status": "ok", "action": action, "message": message}
    if action in ("apagar", "reiniciar"):
        response["delay"] = system_service.SHUTDOWN_DELAY
    return response

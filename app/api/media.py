import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.core.security import require_api_key
from app.services import media_service

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(require_api_key)])

# clave data-action del HTML -> (función del servicio, mensaje al usuario)
ACTIONS: dict[str, tuple] = {
    "vol_up": (media_service.vol_up, "Volumen aumentado"),
    "vol_down": (media_service.vol_down, "Volumen reducido"),
    "mute": (media_service.mute, "Silencio conmutado"),
    "prev": (media_service.prev_track, "Pista anterior"),
    "play_pause": (media_service.play_pause, "Reproducción alternada"),
    "next": (media_service.next_track, "Pista siguiente"),
}


@router.post("/api/media/{action}")
def run_media_action(action: str):
    if action not in ACTIONS:
        logger.warning("Acción multimedia desconocida: %s (válidas: %s)", action, ", ".join(ACTIONS))
        raise HTTPException(status_code=404, detail="Acción desconocida")

    func, message = ACTIONS[action]
    if not func():
        logger.error("La acción multimedia %s no pudo ejecutarse", action)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "action": action, "message": "No se pudo ejecutar la acción"},
        )

    logger.info("Acción multimedia ejecutada: %s", action)
    return {"status": "ok", "action": action, "message": message}

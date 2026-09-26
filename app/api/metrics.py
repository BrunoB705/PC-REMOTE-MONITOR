from fastapi import APIRouter, Depends

from app.core.security import require_api_key
from app.services.metrics import cpu, gpu, memory, motherboard, storage, uptime

router = APIRouter(dependencies=[Depends(require_api_key)])

@router.get("/api/metrics")
def get_metrics():
    return{
        "cpu": {
            "usage": cpu.get_cpu_usage(),
            "temperature": cpu.get_cpu_temperature()
        },
        "gpu": gpu.get_gpu(),
        "motherboard": {
            "temperature": motherboard.get_motherboard_temperature()
        },
        "memory": memory.get_memory(),
        "storage": storage.get_all_storage(),
        "uptime": uptime.get_uptime()
    }
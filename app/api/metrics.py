from fastapi import APIRouter
from app.services.metrics import cpu, memory, storage, uptime

router = APIRouter()

@router.get("/api/metrics")
def get_metrics():
    return{
        "cpu": {
            "usage": cpu.get_cpu_usage(),
            "temperature": cpu.get_cpu_temperature()
        },
        "memory": memory.get_memory(),
        "storage": storage.get_all_storage(),
        "uptime": uptime.get_uptime()
    }
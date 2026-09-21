from pydantic import BaseModel

class Metric(BaseModel):
    name: str
    value: float
    unit: str

class MetricsResponse(BaseModel):
    cpu_percent: float
    ram_percent: float
    disk_percent: float
    uptime: float
    timestamp: str

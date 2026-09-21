from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import metrics
import os

app = FastAPI(title="PC Remote & Monitor")

app.include_router(metrics.router)

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "web", "static")), name="static")

@app.get("/")
def dashboard():
    return FileResponse(os.path.join(os.path.dirname(__file__), "web", "templates", "index.html"))
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import metrics, system, media
from app.services.metrics import manager
import os


@asynccontextmanager
async def lifespan(app):
    manager.open_manager()
    yield
    manager.close_manager()


app = FastAPI(title="PC Remote & Monitor", lifespan=lifespan)

app.include_router(metrics.router)
app.include_router(system.router)
app.include_router(media.router)

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "web", "static")), name="static")

@app.get("/")
def dashboard():
    return FileResponse(
        os.path.join(os.path.dirname(__file__), "web", "templates", "index.html"),
        headers={"Cache-Control": "no-cache"},
    )
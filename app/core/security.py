import secrets

from fastapi import Header, HTTPException

from app.core.config import API_KEY


def require_api_key(x_api_key: str = Header(default="")):
    valid = secrets.compare_digest(x_api_key.encode("utf-8"), API_KEY.encode("utf-8"))
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid API key")

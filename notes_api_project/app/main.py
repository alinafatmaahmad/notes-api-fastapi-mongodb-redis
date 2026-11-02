# ---------- START POINT OF THE APP ----------
# Run with:  uvicorn app.main:app --reload
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routers import notes, auth
from app.services import auth_service
from app.database import mongo_is_working, redis_client

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app):
    if mongo_is_working():
        auth_service.create_default_admin()   # makes admin / admin123 once
    yield


# docs_url=None -> hides the /docs screen, we use our own simple page instead
app = FastAPI(title="Notes App", docs_url=None, redoc_url=None, lifespan=lifespan)

app.include_router(auth.router)
app.include_router(notes.router)


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/status")
def status():
    return {"mongodb": mongo_is_working(), "redis": redis_client is not None}

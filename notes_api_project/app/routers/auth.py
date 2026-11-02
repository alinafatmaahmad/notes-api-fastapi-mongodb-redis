# ---------- ROUTER LAYER: /auth ----------
from fastapi import APIRouter, HTTPException
from app.models.schemas import UserInput
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
def register(user: UserInput):
    if not auth_service.register(user.username, user.password):
        raise HTTPException(status_code=409, detail="Username already exists")
    return {"message": "Registered! Now login."}


@router.post("/login")
def login(user: UserInput):
    result = auth_service.login(user.username, user.password)
    if not result:
        raise HTTPException(status_code=401, detail="Wrong username or password")
    return result

# ---------- SECURITY CHECKS ----------
# FastAPI runs these BEFORE the route function.
from fastapi import Depends, Header, HTTPException
from app.repositories import user_repository


# Authentication: is the user logged in?
def get_current_user(authorization: str = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Please login first")
    user = user_repository.find_by_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token, please login again")
    return user


# Authorization: is the logged-in user an admin?
def admin_only(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can do this")
    return user

# ---------- SERVICE LAYER: LOGIN ----------
# AUTHENTICATION  = "Who are you?"        (login with username + password)
# AUTHORIZATION   = "What can you do?"    (admin can delete, normal user cannot)
# NOTE: sha256 + simple token is only for learning. Real apps use bcrypt + JWT.
import hashlib
import secrets
from app.repositories import user_repository
from app.config import ADMIN_USERNAME, ADMIN_PASSWORD


def _hash(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def create_default_admin():
    if not user_repository.find_by_username(ADMIN_USERNAME):
        user_repository.create({"username": ADMIN_USERNAME,
                                "password": _hash(ADMIN_PASSWORD),
                                "role": "admin"})


def register(username: str, password: str):
    if user_repository.find_by_username(username):
        return False                                   # username already taken
    user_repository.create({"username": username, "password": _hash(password), "role": "user"})
    return True


def login(username: str, password: str):
    user = user_repository.find_by_username(username)
    if not user or user["password"] != _hash(password):
        return None
    token = secrets.token_hex(16)                      # random secret key for this login
    user_repository.save_token(username, token)
    return {"token": token, "username": username, "role": user["role"]}

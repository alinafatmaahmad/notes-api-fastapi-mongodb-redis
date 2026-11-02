# ---------- REPOSITORY LAYER ----------
# ONLY this file talks to the "users" collection in MongoDB.
from app.database import users_collection


def find_by_username(username: str):
    return users_collection.find_one({"username": username})


def find_by_token(token: str):
    return users_collection.find_one({"token": token})


def create(user: dict):
    users_collection.insert_one(user)


def save_token(username: str, token: str):
    users_collection.update_one({"username": username}, {"$set": {"token": token}})

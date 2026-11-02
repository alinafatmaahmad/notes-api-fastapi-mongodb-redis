# ---------- DATABASE CONNECTIONS ----------
# This file connects our API to MongoDB and Redis.
from pymongo import MongoClient
import redis
from app.config import MONGO_URL, DB_NAME, REDIS_HOST, REDIS_PORT

# 1) MongoDB connection  (this is how API talks to MongoDB)
mongo_client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=3000)
db = mongo_client[DB_NAME]
notes_collection = db["notes"]     # like a "table" for notes
users_collection = db["users"]     # like a "table" for users

# 2) Redis connection (optional - app still works if Redis is OFF)
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                               decode_responses=True, socket_connect_timeout=1)
    redis_client.ping()
except redis.exceptions.RedisError:
    redis_client = None


def mongo_is_working():
    try:
        mongo_client.admin.command("ping")
        return True
    except Exception:
        return False

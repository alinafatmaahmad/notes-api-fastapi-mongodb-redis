# ---------- CACHING WITH REDIS ----------
# Idea: asking MongoDB every time is slow. So we keep a copy of the answer in Redis.
#   1st request -> MongoDB (slow)  -> save copy in Redis
#   2nd request -> Redis   (fast)  -> no MongoDB needed
# The copy is deleted after CACHE_SECONDS, and also when notes change.
import json
from app.database import redis_client
from app.config import CACHE_SECONDS


def get_cache(key: str):
    if redis_client is None:
        return None
    value = redis_client.get(key)
    return json.loads(value) if value else None


def set_cache(key: str, data: dict):
    if redis_client is not None:
        redis_client.setex(key, CACHE_SECONDS, json.dumps(data))   # setex = set with expiry time


def clear_notes_cache():
    # Called after create / update / delete, so old data is never shown.
    if redis_client is not None:
        for key in redis_client.scan_iter("notes:*"):
            redis_client.delete(key)

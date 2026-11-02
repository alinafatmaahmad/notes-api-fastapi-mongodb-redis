# ---------- CONFIGURATION ----------
# All settings live in ONE place. Change them here, nowhere else.
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")  # same URL you type in MongoDB Compass
DB_NAME = "notes_app"                                            # database name (you will see it in Compass)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CACHE_SECONDS = 60   # how long Redis remembers a result

ADMIN_USERNAME = "admin"      # default admin, created automatically
ADMIN_PASSWORD = "admin123"

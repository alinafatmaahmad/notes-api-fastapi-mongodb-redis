# ---------- SERVICE LAYER ----------
# Business logic lives here: filtering, sorting, pagination, caching rules.
# It uses the repository (for MongoDB) and cache_service (for Redis).
import math
import re
from app.repositories import note_repository
from app.services import cache_service


def list_notes(search, category, sort_by, order, page, limit):
    # 1) Look in Redis first
    cache_key = f"notes:{search}:{category}:{sort_by}:{order}:{page}:{limit}"
    cached = cache_service.get_cache(cache_key)
    if cached:
        return {**cached, "source": "cache (Redis)"}

    # 2) Not in Redis -> build the MongoDB query
    query = {}
    if search:                                   # FILTER by words in title
        query["title"] = {"$regex": re.escape(search), "$options": "i"}
    if category:                                 # FILTER by category
        query["category"] = category

    sort_order = 1 if order == "asc" else -1     # SORTING
    skip = (page - 1) * limit                    # PAGINATION: skip earlier pages

    total = note_repository.count(query)
    notes = note_repository.find_many(query, sort_by, sort_order, skip, limit)

    result = {
        "notes": notes,
        "total": total,
        "page": page,
        "total_pages": max(1, math.ceil(total / limit)),
    }

    # 3) Save a copy in Redis for next time
    cache_service.set_cache(cache_key, result)
    return {**result, "source": "database (MongoDB)"}


def get_note(note_id):
    return note_repository.find_by_id(note_id)


def create_note(data: dict, username: str):
    data["owner"] = username
    note = note_repository.create(data)
    cache_service.clear_notes_cache()
    return note


def update_note(note_id, data: dict):
    note = note_repository.update(note_id, data)
    cache_service.clear_notes_cache()
    return note


def delete_note(note_id):
    deleted = note_repository.delete(note_id)
    cache_service.clear_notes_cache()
    return deleted

# ---------- REPOSITORY LAYER ----------
# ONLY this file talks to the "notes" collection in MongoDB.
# No business rules here - just save, find, update, delete.
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from app.database import notes_collection


def _clean(doc):
    # MongoDB gives "_id" as ObjectId. We turn it into a simple string "id".
    doc["id"] = str(doc.pop("_id"))
    return doc


def create(data: dict):
    data["created_at"] = datetime.now().isoformat(timespec="seconds")
    result = notes_collection.insert_one(data)
    return find_by_id(str(result.inserted_id))


def find_many(query: dict, sort_field: str, sort_order: int, skip: int, limit: int):
    cursor = (notes_collection.find(query)
              .sort([(sort_field, sort_order), ("_id", 1)])
              .skip(skip)
              .limit(limit))
    return [_clean(doc) for doc in cursor]


def count(query: dict):
    return notes_collection.count_documents(query)


def find_by_id(note_id: str):
    try:
        doc = notes_collection.find_one({"_id": ObjectId(note_id)})
    except InvalidId:
        return None
    return _clean(doc) if doc else None


def update(note_id: str, data: dict):
    try:
        notes_collection.update_one({"_id": ObjectId(note_id)}, {"$set": data})
    except InvalidId:
        return None
    return find_by_id(note_id)


def delete(note_id: str):
    try:
        result = notes_collection.delete_one({"_id": ObjectId(note_id)})
    except InvalidId:
        return False
    return result.deleted_count == 1

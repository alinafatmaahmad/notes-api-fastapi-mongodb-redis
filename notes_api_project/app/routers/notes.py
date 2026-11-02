# ---------- ROUTER LAYER: /notes ----------
# The router only receives the request and sends the response.
# The real work is done by the service.
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.schemas import NoteCreate, NoteUpdate
from app.services import note_service
from app.dependencies import get_current_user, admin_only

router = APIRouter(prefix="/notes", tags=["Notes"])


# GET  -> read many notes (anyone can do this)
@router.get("")
def get_notes(
    search: str = "",
    category: str = "",
    sort_by: Literal["created_at", "title"] = "created_at",
    order: Literal["asc", "desc"] = "desc",
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=20),
):
    return note_service.list_notes(search, category, sort_by, order, page, limit)


# GET  -> read one note
@router.get("/{note_id}")
def get_one_note(note_id: str):
    note = note_service.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# POST -> create (login needed)
@router.post("", status_code=201)
def create_note(note: NoteCreate, user=Depends(get_current_user)):
    return note_service.create_note(note.model_dump(), user["username"])


# PUT  -> update (login needed)
@router.put("/{note_id}")
def update_note(note_id: str, note: NoteUpdate, user=Depends(get_current_user)):
    data = note.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="Nothing to update")
    updated = note_service.update_note(note_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


# DELETE -> only admin
@router.delete("/{note_id}")
def delete_note(note_id: str, admin=Depends(admin_only)):
    if not note_service.delete_note(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted"}

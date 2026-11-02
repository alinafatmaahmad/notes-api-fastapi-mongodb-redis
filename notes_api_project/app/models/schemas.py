# ---------- PYDANTIC MODELS (validation) ----------
# Pydantic checks the data coming from the user.
# If data is wrong, FastAPI automatically sends a 422 error.
from typing import Optional, Literal
from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    content: str = Field(min_length=1, max_length=500)
    category: Literal["study", "work", "personal"] = "study"


class NoteUpdate(BaseModel):
    # all optional: user can change only what they want
    title: Optional[str] = Field(default=None, min_length=3, max_length=50)
    content: Optional[str] = Field(default=None, min_length=1, max_length=500)
    category: Optional[Literal["study", "work", "personal"]] = None


class UserInput(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=4, max_length=30)

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class Note(BaseModel):
    title: str
    description: str


class NoteResult(Note):
    created_at: datetime
    owner: str


class User(BaseModel):
    email: EmailStr
    password: str


class UserResult(BaseModel):
    email: EmailStr
    created_at: datetime = datetime.now()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class EditPassword(BaseModel):
    old_password: str
    new_password: str

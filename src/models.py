from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class Note(BaseModel):
    ''' note creation model '''
    title: str
    description: str


class NoteResult(Note):
    ''' note result for the user '''
    created_at: datetime
    owner: str


class User(BaseModel):
    ''' user creation model '''
    email: EmailStr
    password: str


class UserResult(BaseModel):
    ''' user result for the user '''
    email: EmailStr
    created_at: datetime = datetime.now()


class Token(BaseModel):
    ''' token verif model'''
    access_token: str
    token_type: str


class TokenData(BaseModel):
    ''' check email '''
    email: Optional[str] = None


class EditPassword(BaseModel):
    ''' edit password model '''
    old_password: str
    new_password: str

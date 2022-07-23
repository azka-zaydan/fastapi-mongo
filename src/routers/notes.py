from typing import List
from fastapi import APIRouter, Depends, HTTPException
import database
from models import Note, NoteResult
from oauth2 import get_current_user

router = APIRouter(
    prefix='/notes',
    tags=['Notes']
)


@router.get('/', response_model=List[NoteResult])
async def get_all_notes(current_user: str = Depends(get_current_user)):
    response = await database.fetch_all(current_user)
    return response


@router.get('/{title}', response_model=NoteResult)
async def get_note_by_title(title: str, current_user: str = Depends(get_current_user)):
    response = await database.fetch_by_title(title, current_user)
    if response:
        return response
    raise HTTPException(404, 'Item not found')


@router.post('/', response_model=NoteResult)
async def post_note(note: Note, current_user: str = Depends(get_current_user)):
    response = await database.create_note(note.dict(), current_user)
    if response:
        return response
    raise HTTPException(404, 'Bad payload')


@router.put('/{title}', response_model=Note)
async def update_note(note_title: str, data: str, current_user: str = Depends(get_current_user)):
    response = await database.update_note(note_title, data, current_user)
    if response:
        return response
    raise HTTPException(404, 'Item not found')


@router.delete('/{title}')
async def delete_note(note_title: str, current_user: str = Depends(get_current_user)):
    response = await database.remove_note(note_title, current_user)
    if response:
        return 'item deleted'
    raise HTTPException(404, 'Item not found')

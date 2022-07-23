from fastapi import APIRouter, HTTPException
from models import User, UserResult
import database

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', response_model=UserResult)
async def create_user(user: User):

    result = await database.create_user(user.dict())
    if result:
        return result
    raise HTTPException(404, 'User already exist')


@router.get('/{email}', response_model=UserResult)
async def find_user_by_email(email: str):
    response = await database.find_user(email)
    if response:
        return response
    raise HTTPException(404, 'User not found')

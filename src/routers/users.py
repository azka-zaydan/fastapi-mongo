from calendar import c
from fastapi import APIRouter, Depends, HTTPException
from src.models import EditPassword, User, UserResult
import src.database as database
from src.oauth2 import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', response_model=UserResult)
async def create_user(user: User, current_user=Depends(get_current_user)):
    ''' create user '''
    print(current_user)
    if current_user['role'] == 'user':
        raise HTTPException(404, 'you dont have access')

    result = await database.create_user(user.dict())
    if result:
        return result
    raise HTTPException(404, 'User already exist')


@router.get('/{email}', response_model=UserResult)
async def find_user_by_email(email: str, current_user=Depends(get_current_user)):
    ''' find user by email '''

    if current_user['role'] == 'user':
        raise HTTPException(404, 'you dont have access')

    response = await database.find_user(email)
    if response:
        return response
    raise HTTPException(404, 'User not found')


@router.put('/',)
async def change_password(passwords: EditPassword, current_user: str = Depends(get_current_user)):
    ''' change user passowrd '''
    response = await database.change_user_password(passwords.dict(), current_user['email'])
    if response:
        return response
    raise HTTPException(404, 'Invalid credentials')


@ router.delete('/')
async def delete_user(email: str, current_user: str = Depends(get_current_user)):
    ''' delete user '''

    if current_user['role'] == 'user':
        raise HTTPException(404, 'you dont have access')

    response = await database.delete_user(email)
    if response != None:
        return response
    raise HTTPException(404, "User not found")

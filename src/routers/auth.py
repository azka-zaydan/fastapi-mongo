from fastapi import APIRouter, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import database
from oauth2 import create_access_token
from util import verify

router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)


@router.post('/')
async def user_login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    print(user_credentials)
    find = await database.find_user(user_credentials.username)
    print(find)
    if find:
        if verify(user_credentials.password, find['password']):
            access_token = create_access_token(
                data={"user_email": user_credentials.username})
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        raise HTTPException(404, 'Invalid credentials')
    raise HTTPException(404, 'User not found')

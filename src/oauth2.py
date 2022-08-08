from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.models import TokenData
import src.database as database
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


def create_access_token(data: dict):
    ''' create access token for auth'''
    to_encode = data.copy()
    expire = str(datetime.utcnow() +
                 timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"expiration": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_access_token(token: str, credentials_exception: HTTPException):
    ''' verify access token '''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get('user_email')
        if user_email is None:
            raise credentials_exception
        token_data = TokenData(email=user_email)
    except JWTError as exc:
        raise credentials_exception from exc
    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme),):
    ''' get current user '''
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                          detail='could not validate credentials', headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = await database.find_user(token.email)
    if user:
        return user
    raise HTTPException(404, 'Please log in')

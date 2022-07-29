from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashpass(password: str):
    ''' hashpasswords '''
    return pwd_context.hash(password)


def verify(password: str, hashed_password: str):
    ''' verify hashed passwords '''
    return pwd_context.verify(password, hashed_password)

# app/auth.py
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

from app import models, config
from app.crud import get_user_by_id
from databases import Database
from app.database import database

# Load env 
load_dotenv()

SECRET_KEY= os.getenv('SECRET_KEY', 'MY-EYES-ARE-UP-HERE')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRATION_MINS = int(os.getenv('ACCESS_TOKEN_EXPIRATION_MINS', 30))

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

def hash_pwd(password: str) -> str: 
    return pwd_context.hash(password)

def verify_pwd(plain_password: str, hashed_password: str) -> bool: 
    return pwd_context.verify(plain_password, hashed_password)

# JWT Creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None): 
    to_encode = data.copy() # create shallow copy 
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINS))
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# JWT Verification
def verify_access_token(token: str): 
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
# Check users JWT
async def get_current_user(token: str = Depends(oauth_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate user credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('user_id')
        if user_id is None: 
            raise credentials_exception
    except JWTError: 
        raise credentials_exception
    
    user = await get_user_by_id(user_id=user_id)
    if user is None: 
        raise credentials_exception
    return user
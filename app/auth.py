# app/auth.py
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

from app.crud import get_user_by_id

# Load env 
load_dotenv()

# pull env variables 
SECRET_KEY= os.getenv('SECRET_KEY', 'MY-EYES-ARE-UP-HERE')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRATION_MINS = int(os.getenv('ACCESS_TOKEN_EXPIRATION_MINS', 30))

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
app_oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

# handle hasing a user password to be stored in the database 
def hash_pwd(password: str) -> str: 
    return pwd_context.hash(password)


# handle dehashing and comparing a user's password during login 
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
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    
# Check users JWT, used for user specific api calls
async def get_current_user(token: str = Depends(app_oauth_scheme)) -> dict:
    
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get('sub'))
        if user_id is None: 
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError: 
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = await get_user_by_id(user_id=user_id)
    if user is None: 
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user
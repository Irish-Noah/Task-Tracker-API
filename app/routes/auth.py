# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserCreate, UserOut, UserLogin, Token
from app import crud, auth
from app.database import database
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/register', response_model=UserOut)
async def register(user: UserCreate): 
    # Make sure user doesn't already exist
    existing_user = await crud.get_user_by_username(user.username)
    if existing_user: 
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = await crud.get_user_by_email(user.email)
    if existing_email: 
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash pwd and create a new user
    hashed_pwd = auth.hash_pwd(user.password)
    new_user = await crud.create_user(user, hashed_pwd)
    return new_user


@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_record = await crud.get_user_by_username(form_data.username)
    if not user_record: 
        raise HTTPException(status_code=400, detail="Invalid username or passsword")
    
    # Validate password 
    if not auth.verify_pwd(form_data.password, user_record['password']):
        raise HTTPException(status_code=400, detail='Invalid username or password')
    
    # Create and return token 
    access_token = auth.create_access_token(data={'sub': str(user_record['id'])})
    return {'access_token': access_token, 'token_type': 'bearer'}
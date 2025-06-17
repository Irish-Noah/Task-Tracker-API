# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserOut, Token, UserBase
from app.auth import hash_pwd, verify_pwd, create_access_token
from app.crud import get_user_by_username, get_user_by_email, create_user
from app.database import database
from fastapi.security import OAuth2PasswordRequestForm

# Set the api route prefix to 'auth' and set the Swagger group to 'Auth'
router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

# handle the new user registration api call 
@router.post('/register', response_model=UserBase)
async def register(user: UserCreate):
    # Make sure user doesn't already exist
    existing_user = await get_user_by_username(user.username)
    if existing_user: 
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = await get_user_by_email(user.email)
    if existing_email: 
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash pwd and create a new user
    hashed_pwd = hash_pwd(user.password)
    new_user = await create_user(user, hashed_pwd)
    return new_user


# handle the user login api call
@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Make sure user exists before checking password 
    user_record = await get_user_by_username(form_data.username)
    if not user_record: 
        raise HTTPException(status_code=400, detail="Invalid username or passsword")
    
    # Validate password 
    if not verify_pwd(form_data.password, user_record['password']):
        raise HTTPException(status_code=400, detail='Invalid username or password')
    
    # Create and return JWT 
    access_token = create_access_token(data={'sub': str(user_record['id'])})
    return {'access_token': access_token, 'token_type': 'bearer'}
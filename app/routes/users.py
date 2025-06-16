# app/routes/users.py
from fastapi import APIRouter, HTTPException
from app.schemas import UserOut
from app.crud import get_user_by_username, get_user_by_email, get_user_by_id, get_user_tasks, get_users, delete_user_by_username
# create user handled in app/routes/auth/register

router = APIRouter(
    tags=['Users']
)

@router.get('/users/', response_model=list[UserOut])
async def get_all_users(): 
    users = await get_users()
    if not users: 
        raise HTTPException(status_code=404, detail='No users found')
    return users

@router.get('/users/{user_id}', response_model=UserOut)
async def user_by_id(user_id: int): 
    user = await get_user_by_id(user_id)
    if user is None: 
        raise HTTPException(status_code=404, detail="No user found with that ID")
    return user 

@router.get('/users/{email}', response_model=UserOut)
async def user_by_email(user_email: str): 
    user = await get_user_by_email(user_email)
    if user is None: 
        raise HTTPException(status_code=404, detail="No user found with that email")
    return user 

@router.get('/users/{username}', response_model=UserOut)
async def user_by_username(username: str): 
    user = await get_user_by_username(username)
    if user is None: 
        raise HTTPException(status_code=404, detail="No user found with that username")
    return user 

@router.delete('/users/{username}', response_model=None)
async def delete_user(username: str): 
    user = await get_user_by_username(username)
    if user is None: 
        raise HTTPException(status_code=404, detail="No user found with that ID")
    await delete_user_by_username(username)
    raise HTTPException(status_code=200, detail=f"User {username} deleted successfully!")

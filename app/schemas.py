# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

''' Task Object Schemas'''

# Create Task object
class TaskCreate(BaseModel): 
    title: str
    description: Optional[str] = None
    completed: bool = False

# Update existing Task object
class TaskUpdate(BaseModel):
    title: str = None
    description: Optional[str] = None
    completed: bool = False

# Get Task object from db
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    user_id: int

    class Config:
        from_attributes = True

# GET Task object from db 
class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        from_attributes = True


''' User Object Schemas '''

# Basic User object
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Register User object
class UserCreate(UserBase):
    password: str

# Get User object from db 
class UserOut(UserBase):
    id: int
    username: str
    email: str
    password: str # Needs to be dehashed for admin display

    class Config: 
        from_attributes = True # conver to JSON


''' User Auth Schemas'''

# Expected User object for login 
class UserLogin(BaseModel):
    username: str
    password: str

# Token object for post login tasks
class Token(BaseModel):
    access_token: str
    token_type: str
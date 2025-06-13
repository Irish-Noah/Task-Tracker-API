# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

''' Task Object Schemas'''

# Incoming data (client -> task)
class TaskCreate(BaseModel): 
    title: str
    description: Optional[str] = None
    completed: bool = False

# Update Task Object
class TaskUpdate(BaseModel):
    title: str = None
    description: Optional[str] = None
    completed: bool = False

# Outgoing data (task -> client)
class Task(TaskCreate):
    id: int
    title: str

    class Config: 
        from_attributes = True # convert to JSON


''' User Object Schemas '''

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config: 
        from_attributes = True # conver to JSON


''' User Auth Schemas'''

class UserLogin(BaseModel):
    username: str
    pasword: str

class Token(BaseModel):
    access_token: str
    token_type: str
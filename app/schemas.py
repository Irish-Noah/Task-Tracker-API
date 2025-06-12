# app/schemas.py
from pydantic import BaseModel
from typing import Optional

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
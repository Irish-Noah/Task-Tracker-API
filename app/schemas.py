# app/schemas.py
from pydantic import BaseModel

# Incoming data (client -> task)
class TaskCreate(BaseModel): 
    title: str
    description: str = ''

# Outgoing data (task -> client)
class Task(TaskCreate):
    id: int
    completed: bool

    class Config: 
        orm_mode = True # convert to JSON
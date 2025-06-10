# app/routes/tasks.py
from fastapi import APIRouter
from app.schemas import TaskCreate, Task
from app.crud import create_task

router = APIRouter()

@router.post('/', response_model=Task)
async def create(task: TaskCreate):
    return await create_task(task)
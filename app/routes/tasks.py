# app/routes/tasks.py
from fastapi import APIRouter, HTTPException
from app.schemas import TaskCreate, Task, TaskUpdate
from app.crud import create_task, get_tasks, get_task_by_id, update_task_by_id, delete_all, delete_by_id

router = APIRouter()

@router.post('/', response_model=Task)
async def create(task: TaskCreate):
    return await create_task(task)

@router.get('/tasks/', response_model=list[Task])
async def read_tasks(): 
    return await get_tasks()

@router.get('/tasks/{task_id}', response_model=Task)
async def task_by_id(task_id: int): 
    task = await get_task_by_id(task_id)
    if task is None: 
        raise HTTPException(status_code=404, detail="No task found with that ID")
    return task 

@router.put('/tasks/{task_id}', response_model=Task)
async def update_task(task_id: int, task: TaskUpdate):
    old_task = await get_task_by_id(task_id)
    if old_task is None: 
        raise HTTPException(status_code=404, detail="No task found with that ID")
    await update_task_by_id(task_id, task)
    updated_task = await get_task_by_id(task_id)
    return updated_task

@router.delete('/tasks/', response_model=None)
async def delete_all_tasks():
    await delete_all()
    raise HTTPException(status_code=200, detail="Successfully delete all tasks")

@router.delete('/tasks/{task_id}', response_model=None)
async def delete_task_by_id(task_id: int): 
    old_task = await get_task_by_id(task_id)
    if old_task is None: 
        raise HTTPException(status_code=404, detail="No task found with that ID")
    await delete_by_id(task_id)
    raise HTTPException(status_code=200, detail=f"Task {task_id} deleted successfully!")
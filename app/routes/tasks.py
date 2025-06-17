# app/routes/tasks.py
from fastapi import APIRouter, HTTPException
from app.schemas import TaskCreate, Task, TaskUpdate
from app.crud import create_task, get_user_tasks, get_tasks, get_task_by_id, update_task_by_id, delete_all, delete_by_id

# Set Swagger group for these apis as "Tasks"
router = APIRouter(
    tags=['Tasks']
)

# handle the basic task creation api call 
@router.post('/', response_model=Task)
async def create(task: TaskCreate):
    return await create_task(task, user_id=1)


# handle reading tasks created by a user, keyed off by the user's ID
@router.get('/tasks/{user_id}', response_model=list[Task])
async def read_tasks_by_user(user_id: int): 
    tasks = await get_user_tasks(user_id)
    if not tasks: 
        raise HTTPException(status_code=404, detail=f'No tasks created by user {user_id}')
    return await get_user_tasks(user_id)


# handle reading all tasks, independent from user ownership (admin view)
@router.get('/tasks/', response_model=list[Task])
async def read_tasks(): 
    tasks = await get_tasks()
    if not tasks: 
        raise HTTPException(status_code=404, detail='No tasks found in table')
    return tasks


# handle getting a task by its ID
@router.get('/tasks/{task_id}', response_model=Task)
async def task_by_id(task_id: int): 
    task = await get_task_by_id(task_id)
    if task is None: 
        raise HTTPException(status_code=404, detail="No task found with that ID")
    return task 


# handle updating the contents of a task by its ID
@router.put('/tasks/{task_id}', response_model=Task)
async def update_task(task_id: int, task: TaskUpdate):
    old_task = await get_task_by_id(task_id)
    if old_task is None: 
        raise HTTPException(status_code=404, detail="No task found with that ID")
    await update_task_by_id(task_id, task)
    updated_task = await get_task_by_id(task_id)
    return updated_task


# handle deleting all tasks 
@router.delete('/tasks/', response_model=None)
async def delete_all_tasks():
    await delete_all()
    raise HTTPException(status_code=200, detail="Successfully delete all tasks")


# handle deleting a task by its ID
@router.delete('/tasks/{task_id}', response_model=None)
async def delete_task_by_id(task_id: int): 
    old_task = await get_task_by_id(task_id)
    if old_task is None: 
        raise HTTPException(status_code=404, detail="No task found with that ID")
    await delete_by_id(task_id)
    raise HTTPException(status_code=200, detail=f"Task {task_id} deleted successfully!")
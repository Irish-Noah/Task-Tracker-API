# app/routes/tasks.py
from fastapi import APIRouter, HTTPException, Depends
from app.schemas import TaskCreate, Task, TaskUpdate, TaskOut
from app.crud import create_task, get_user_tasks, get_tasks, get_task_by_title, update_task_by_name, delete_all, delete_by_id
from app.auth import get_current_user

# Set Swagger group for these apis as "Tasks"
router = APIRouter(
    tags=['Tasks']
)

# handle the basic task creation api call 
@router.post('/', response_model=TaskOut)
async def create(task: TaskCreate, current_user: dict = Depends(get_current_user)):
    return await create_task(task, current_user['id'])


# handle reading tasks created by a user, keyed off by the user's ID
@router.get('/my-tasks', response_model=list[TaskOut])
async def read_tasks_by_user(current_user: dict = Depends(get_current_user)): 
    user_id = current_user['id']
    tasks = await get_user_tasks(user_id)
    if not tasks:
        raise HTTPException(status_code=404, detail=f'No tasks created by user {user_id}')
    return tasks


# handle reading all tasks, independent from user ownership (admin view)
@router.get('/tasks', response_model=list[TaskOut])
async def read_tasks(current_user: dict = Depends(get_current_user)): 
    user_id = current_user['id']
    if user_id != 2: 
        raise HTTPException(status_code=403, detail='Attempting to access an admin API call')
    tasks = await get_tasks()
    if not tasks: 
        raise HTTPException(status_code=404, detail='No tasks found in table')
    return tasks


# handle getting a task by its name
@router.get('/tasks/{task_name}', response_model=TaskOut)
async def task_by_title(task_name: str, current_user: dict = Depends(get_current_user)): 
    user_id = current_user['id']
    task = await get_task_by_title(task_name, user_id)
    if task is None: 
        raise HTTPException(status_code=404, detail="No task found with that name")
    return task


# handle updating the contents of a task by its name
@router.put('/tasks/{task_name}', response_model=TaskOut)
async def update_task(task_name: str, task: TaskUpdate, current_user: dict = Depends(get_current_user)):
    user_id = current_user['id']
    old_task = await get_task_by_title(task_name, user_id)
    if old_task is None: 
        raise HTTPException(status_code=404, detail="No task found with that name")
    await update_task_by_name(task_name, task, user_id)
    updated_task = await get_task_by_title(task_name, user_id)
    return updated_task


# handle deleting all tasks 
@router.delete('/tasks/', response_model=None)
async def delete_all_tasks():
    await delete_all()
    raise HTTPException(status_code=200, detail="Successfully delete all tasks")


# handle deleting a task by its ID
@router.delete('/tasks/{task_name}', response_model=None)
async def delete_task_by_id(task_name: str, current_user: dict = Depends(get_current_user)): 
    user_id = current_user['id']
    old_task = await get_task_by_title(task_name, user_id)
    if old_task is None: 
        raise HTTPException(status_code=404, detail="No task found with that ID")
    await delete_by_id(task_name, user_id)
    raise HTTPException(status_code=200, detail=f"Task {task_name} deleted successfully!")
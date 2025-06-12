# app/crud.py
from sqlalchemy import select, delete, update
from app.models import tasks
from app.schemas import TaskCreate, TaskUpdate
from app.database import database 

# Create a new task object 
async def create_task(task: TaskCreate): 
    query = tasks.insert().values(
        title=task.title,
        description=task.description,
        completed=False
    )
    task_id = await database.execute(query)
    # dictionary unpacking syntax and adds two fields (id, completed)
    return {**task.dict(), "id": task_id, "completed": False}

# Get all tasks 
async def get_tasks(): 
    query = select(tasks)
    return await database.fetch_all(query)

# Get task by ID
async def get_task_by_id(task_id): 
    query = select(tasks).where(tasks.c.id == task_id)
    return await database.fetch_one(query)

# Update a task by ID
async def update_task_by_id(task_id, task: TaskUpdate): 
    query = update(tasks).where(tasks.c.id == task_id).values(
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    return await database.execute(query)

# Delete all tasks
async def delete_all(): 
    query = delete(tasks)
    return await database.execute(query)

# Delete a task by ID
async def delete_by_id(task_id): 
    query = delete(tasks).where(tasks.c.id == task_id)
    return await database.execute(query)
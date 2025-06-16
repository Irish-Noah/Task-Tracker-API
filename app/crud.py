# app/crud.py
from sqlalchemy import select, delete, update
from app.models import tasks, users
from app.schemas import TaskCreate, TaskUpdate, UserCreate
from app.database import database 

''' Task Object API Calls '''

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


''' User Object API Calls '''

# Create a new user object
async def create_user(user: UserCreate, password: str): 
    query = users.insert().values(
        username=user.username,
        email=user.email, 
        password=user.password
    )
    user_id = await database.execute(query)
    return {**user.dict(exclude={'password'}), 'id': user_id}

# Get user by their unique username
async def get_user_by_username(username: str):
    query = select(users).where(users.c.username == username)
    return await database.fetch_one(query)

# Get user by their unique email 
async def get_user_by_email(email: str): 
    query = select(users).where(users.c.email == email)
    return await database.fetch_one(query)

# Get user by their ID
async def get_user_by_id(user_id: int):
    query = select(users).where(users.c.id == user_id)
    return await database.fetch_one(query)

# Get all users 
async def get_users():
    return await database.fetch_all(query=select(users))

# Delete user by their unique username 
async def delete_user_by_username(username: str): 
    # TODO: Will need to delete all tasks associated to users with this call later
    query = delete(users).where(users.c.username == username)
    return await database.execute(query)

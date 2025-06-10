# app/crud.py
from app.models import tasks
from app.schemas import TaskCreate
from app.database import database 

async def create_task(task: TaskCreate): 
    query = tasks.insert().values(
        title=task.title,
        description=task.description,
        completed=False
    )
    task_id = await database.execute(query)
    # dictionary unpacking syntax and adds two fields (id, completed)
    return {**task.dict(), "id": task_id, "completed": False}
# app/main.py
from fastapi import FastAPI
from app.database import database
from app.routes import tasks, users, auth

app = FastAPI()

# Link apis into project
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.on_event('startup')
async def startup(): 
    await database.connect()

@app.on_event('shutdown')
async def shutdown(): 
    await database.disconnect()

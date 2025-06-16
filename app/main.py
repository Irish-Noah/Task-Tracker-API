# app/main.py
from fastapi import FastAPI
from app.database import database
from app.routes import tasks, users, auth

app = FastAPI()

# Create our routes
#app.include_router(users.router, prefix="/auth", tags=["Auth"])
#app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

app.include_router(tasks.router)
app.include_router(auth.router)

@app.on_event('startup')
async def startup(): 
    await database.connect()

@app.on_event('shutdown')
async def shutdown(): 
    await database.disconnect()

@app.get('/')
def root(): 
    return {'message': "Hello World"}

import asyncio
from app.models import metadata
from app.database import engine, database

# one time run, just creates the table from the database.py file
async def create_tables(): 
    async with engine.begin() as conn: 
        await conn.run_sync(metadata.create_all)
asyncio.run(create_tables())
# app/database.py 
from databases import Database
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

# Create sqlite db file
DATABASE_URL = "sqlite+aiosqlite:///./tasktracker.db"
database = Database(DATABASE_URL)

engine: AsyncEngine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()
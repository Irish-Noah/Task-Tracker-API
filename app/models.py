# app/models.py
from sqlalchemy import Table, Column, Integer, String, Boolean
from app.database import metadata

# Create the task table layout
tasks = Table(
    "tasks",
    metadata, 
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String),
    Column('completed', Boolean, default=False)
)
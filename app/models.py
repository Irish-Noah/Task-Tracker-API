# app/models.py
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
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

# Create the user table layout
users = Table(
    "users",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True, index=True, nullable=False),
    Column('email', String, unique=True, index=True, nullable=False),
    Column('password', String, nullable=False)
)
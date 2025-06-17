## Task Tracker API Project
I want to keep my skills sharp and explore new stacks, so this is my first attempt a project using a new stack! 

Goal: A simple checklist that persists data between sessions and database connections

Stretch Goal: User auth and user specific lists (achieved!), would be cool to attach to my github website too

### Stack: 
- Python (using a virtual env)
- FastAPI
- SQLite

 ### Project Breakdown:
- main.py -> Entry point for the FastAPI app, creates routes and connections to the database
- database.py -> Manages the database connections and shared metadata for SQLAlchemy
- models.py -> Defines the database table structures using SQLAlchemy 
- schemas.py -> Defines data validation using Pydantic models 
- crud.py -> Contains reusable functions for interacting with the database (Create, Read, Update, and Delete)
- auth.py -> Handles user auth logic 
- config.py -> Stores global variables for the app 
- routes/users.py -> Defines endpoints related to user information retrieval
- routes/tasks.py -> Defines endpoints for CRUD tasks  
- routes/auth.py -> Defines endpoints related to user login, tokens, and registration

### Project Accomplishments
- Users can be registered and stored with a hashed password in the database
- Users can login with a timed JWT to see and modify their list of tasks (and can only see their own user specific list of tasks)
- Admin users have oversight of all user lists and tasks 
- Tasks and users persist between sessions
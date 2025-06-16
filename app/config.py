# app/config.py
import os 
from dotenv import load_dotenv
from datetime import timedelta

# load env file into project
load_dotenv()

SECRET_KEY= os.getenv('SECRET_KEY', 'MY-EYES-ARE-UP-HERE')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRATION_MINS = int(os.getenv('ACCESS_TOKEN_EXPIRATION_MINS', 30))
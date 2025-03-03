import os
from dotenv import load_dotenv

load_dotenv()

env_vars= {
    'DATABASE_URL': os.getenv('DATABASE_URL'),
    'SUPERUSER_DATABASE_URL': os.getenv('DATABASE_URL'),
    'DATABASE_NAME': os.getenv('DATABASE_NAME')
}
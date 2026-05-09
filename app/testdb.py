from app.database import engine
from fastapi import FastAPI, Depends

from models import users

try:
    connection = engine.connect()
    print("MySQL Connected Successfully")
    connection.close()
except Exception as e:
    print("DB Connection Error:", e)



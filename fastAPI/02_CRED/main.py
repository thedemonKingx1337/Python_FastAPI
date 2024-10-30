from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
# fastAPI\02 CRED\model\tableModels.py , schemas.py
from .model import schemas, tableModels

# fastAPI\02 CRED\database\database.py
# importing the engine object (presumably created in database.py) from the database module
from .database.database import engine, SessionLocal

# importing Hashing file
from . import hashing

from sqlalchemy.orm import Session
from typing import List

from .routers import blog, users, login


app = FastAPI()

app.include_router(login.router)
app.include_router(blog.router)
app.include_router(users.router)

tableModels.Base.metadata.create_all(bind=engine)

from fastapi import APIRouter, status, Depends,  HTTPException
from typing import List
from sqlalchemy.orm import Session

from ..model import schemas, tableModels
from ..database.database import engine, SessionLocal
from ..database.database import get_db
from .. import hashing
from .. methods import user
from .. import OAuth2


router = APIRouter(tags=["users"])

# user data N hashing password


@router.post("/user", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):

    return user.create_user(request, db)

# fetching user data with specified id


@router.get("/user{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(OAuth2.get_current_user)):
    return user.get_user(db,  id)

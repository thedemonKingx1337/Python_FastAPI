from fastapi import APIRouter, status, Depends,  HTTPException
from typing import List
from sqlalchemy.orm import Session

from ..model import schemas, tableModels
from ..database.database import engine, SessionLocal
from ..database.database import get_db
from .. import hashing


router = APIRouter(tags=["users"])

# user data N hashing password


@router.post("/user", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):

    new_user = tableModels.User(name=request.name,
                                email=request.email,
                                password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# fetching user data with specified id


@router.get("/user{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(tableModels.User).filter(tableModels.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} not found")
    return user

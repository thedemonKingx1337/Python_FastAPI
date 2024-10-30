from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from ..model import tableModels, schemas
from .. import hashing


def create_user(request: schemas.User, db: Session):
    new_user = tableModels.User(name=request.name,
                                email=request.email,
                                password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session,  id: int):
    user = db.query(tableModels.User).filter(tableModels.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} not found")
    return user

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from ..model import schemas, tableModels
from ..database import database
from ..hashing import Hash
from .. import JWTtoken as token


router = APIRouter(
    tags=['login']
)


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(tableModels.User).filter(
        tableModels.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {request.username} not authenticated")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {request.username} not authenticated")

    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires)
    return schemas.Token(access_token=access_token, token_type="bearer")

    # now we need to generate JWT token and return

    # return user

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


from ..model import schemas, tableModels
from ..database import database
from ..hashing import Hash

router = APIRouter(
    tags=['login']
)


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(tableModels.User).filter(
        tableModels.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {request.username} not authenticated")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {request.username} not authenticated")

    # now we need to generate JWT token and retuen

    return user

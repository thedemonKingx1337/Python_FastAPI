from fastapi import APIRouter, status, Depends, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ..model import schemas, tableModels
from ..database.database import engine, SessionLocal
from ..database.database import get_db
from ..methods import blog
from .. import OAuth2

router = APIRouter(tags=["blogs"])


# store data on the database


@router.post("/blog", status_code=status.HTTP_201_CREATED, )
def create(request: schemas.Blog, db: Session = Depends(get_db), OAuth2_user: schemas.User = Depends(OAuth2.get_current_user)):

    return blog.new_blog(db, request)


# read all data from the database with response model


@router.get("/blog", response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db), OAuth2_user: schemas.User = Depends(OAuth2.get_current_user)):
    return blog.get_all(db)

# filtering and fetching data from db with passed data


@router.get("/blog/{id}", status_code=200,  response_model=schemas.ShowBlog)
def show(id: int, response: Response, db: Session = Depends(get_db), OAuth2_user: schemas.User = Depends(OAuth2.get_current_user)):

    return blog.show(db, id)


# Delete data from the database
@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, )
def destroy(id: int, db: Session = Depends(get_db), OAuth2_user: schemas.User = Depends(OAuth2.get_current_user)):
    return blog.destroy(db, id)


# update an existing date
@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowBlog, )
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db), OAuth2_user: schemas.User = Depends(OAuth2.get_current_user)):
    return blog.update(id, db,  request)

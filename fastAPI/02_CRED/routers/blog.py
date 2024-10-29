from fastapi import APIRouter, status, Depends, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ..model import schemas, tableModels
from ..database.database import engine, SessionLocal
from ..database.database import get_db


router = APIRouter(tags=["blogs"])


# store data on the database


@router.post("/blog", status_code=status.HTTP_201_CREATED, )
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = tableModels.Blog(
        title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# read all data from the database with response model


@router.get("/blog", response_model=List[schemas.ShowBlog], )
def all(db: Session = Depends(get_db)):
    blogs = db.query(tableModels.Blog).all()
    return blogs

# filtering and fetching data from db with passed data


@router.get("/blog/{id}", status_code=200,  response_model=schemas.ShowBlog)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(tableModels.Blog).filter(tableModels.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with {id} not found")
    #    response.status_code = 404
    #    return {"details": f"Blog with id not found{id}"}
    return blog


# Delete data from the database
@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, )
def destroy(id: int, db: Session = Depends(get_db)):
    # Query to find the blog with the given ID
    blog = db.query(tableModels.Blog).filter(tableModels.Blog.id == id)

    # If the blog doesn't exist, raise a 404 error
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {id} not found"
        )

    # Delete the blog if it exists
    blog.delete(synchronize_session=False)

    # Commit the changes to the database
    db.commit()

    # Return a success message
    return {"Done": f"Blog with ID {id} deleted"}


# update an existing date
@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowBlog, )
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(tableModels.Blog).filter(tableModels.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with {id} not found")
    blog.update(request)
    db.commit()
    return {"Done": f"Blog with {id} updated"}

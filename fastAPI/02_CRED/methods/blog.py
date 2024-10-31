
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from ..model import tableModels, schemas


def new_blog(db: Session, request: schemas.Blog):
    new_blog = tableModels.Blog(
        title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_all(db: Session):

    blogs = db.query(tableModels.Blog).all()
    return blogs


def show(db: Session, id: int):
    blog = db.query(tableModels.Blog).filter(tableModels.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with {id} not found")
    #    response.status_code = 404
    #    return {"details": f"Blog with id not found{id}"}
    return blog


def destroy(db: Session, id: int):
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


def update(id: int, db: Session, request: schemas.Blog):
    blog = db.query(tableModels.Blog).filter(tableModels.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with {id} not found")
    blog.update(request.dict())
    db.commit()
    return {"Done": f"Blog with {id} updated"}

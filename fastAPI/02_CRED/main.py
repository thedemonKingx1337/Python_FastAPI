from fastapi import FastAPI, Depends, status, Response, HTTPException
# fastAPI\02 CRED\model\tableModels.py , schemas.py
from .model import schemas, tableModels

# fastAPI\02 CRED\database\database.py
# importing the engine object (presumably created in database.py) from the database module
from .database.database import engine, SessionLocal


from sqlalchemy.orm import Session


app = FastAPI()

tableModels.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# store data on the database


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = tableModels.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# read all data from the database


@app.get("/blog")
def all(db: Session = Depends(get_db)):
    blogs = db.query(tableModels.Blog).all()
    return blogs

# filtering and fetching data from db with passed data


@app.get("/blog/{id}", status_code=200)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(tableModels.Blog).filter(tableModels.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with {id} not found")
    #    response.status_code = 404
    #    return {"details": f"Blog with id not found{id}"}
    return blog


# Delete data from the database
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(tableModels.Blog).filter(tableModels.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with {id} not found")
    blog.update(request)
    db.commit()
    return {"Done": f"Blog with {id} updated"}

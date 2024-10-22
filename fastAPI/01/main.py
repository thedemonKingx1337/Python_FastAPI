from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def about():
    return {"message": "Welcome to the FastAPI API!"}


@app.get("/about")
def info():
    return {"message": "Joseinte ANDI!"}


@app.get("/blog/{id}")
def blog(id):
    return {"id": id, "title": f"Blog Post {id}"}


@app.get("/blogg")
def blogg(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data":  f"{limit}Published Blogs from DB"}
    else:
        return {"data":  f"{limit}Un Published from DB"}


@app.get("/blog_int/unpublished")
def blog_intUnpublished():

    return {"id": "01", "title": "UnPublished"}


@app.get("/blog_int/{id}")
def blog_int(id: int):
    return {"id": id, "title": f"Blog Post {id}"}


class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool]


@app.post("/blogger")
def create_blogger(request: Blog):
    return {"data": f"Blogger is created with with title {request.title}"}

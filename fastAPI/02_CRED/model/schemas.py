from pydantic import BaseModel
from typing import List


class Login(BaseModel):
    username: str
    password: str


class Blog(BaseModel):
    title: str
    body: str


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        from_attributes = True


class ShowBlog(Blog):
    class Config():
        from_attributes = True

    owner: ShowUser


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

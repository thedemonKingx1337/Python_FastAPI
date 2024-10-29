from sqlalchemy import Column, Integer, String, ForeignKey
from ..database.database import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)

    # Add a foreign key to the User table's id column
    user_id = Column(Integer, ForeignKey("users.id"))

    # setting relationship between User and Blog table
    owner = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blog", back_populates="owner")

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the SQLite database URL
SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'

# Create an engine that connects to the SQLite database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory bound to this engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for the declarative models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./habit_tracker.db"

# Connection to the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Class for Tables
Base = declarative_base()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from pathlib import Path

# Manually find and load the .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Load the DATABASE_URL directly from the environment
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file. Please check your configuration.")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- THIS FUNCTION WAS MISSING. IT IS NOW RESTORED. ---
def get_db():
    """
    FastAPI dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
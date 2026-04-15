from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
DB_USER = os.getenv("PS_USERNAME")
DB_PASSWORD = os.getenv("PS_PASSWORD")
DB_HOST = os.getenv("PS_URL")
DB_PORT = os.getenv("PS_PORT")
DB_NAME = os.getenv("PS_DB")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise RuntimeError("Missing one or more PostgreSQL environment variables: PS_USERNAME, PS_PASSWORD, PS_URL, PS_PORT, PS_DB")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
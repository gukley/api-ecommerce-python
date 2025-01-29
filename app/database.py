from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL
from app.utils.models import load_models

engine = create_engine(DATABASE_URL, connect_args={})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
load_models()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

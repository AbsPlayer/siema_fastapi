import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
ModelBase = declarative_base(name="ModelBase")


def get_database() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

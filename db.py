from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine
import os

sqlite_url = os.getenv("DATABASE_URL")

engine = create_engine(sqlite_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


CurrentSession = Annotated[Session, Depends(get_session)]

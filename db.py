from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


CurrentSession = Annotated[Session, Depends(get_session)]

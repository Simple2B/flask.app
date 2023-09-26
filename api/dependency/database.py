from typing import Generator

from sqlalchemy.orm import Session

from app.database import db


def get_db() -> Generator[Session, None, None]:
    with db.Session() as session:
        yield session

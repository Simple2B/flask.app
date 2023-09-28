from typing import Generator
from config import config
from sqlalchemy.orm import Session

CFG = config()

if CFG.IS_API:
    from alchemical import Alchemical
else:
    from alchemical.flask import Alchemical

db = Alchemical()

if CFG.IS_API:
    db.initialize(url=CFG.ALCHEMICAL_DATABASE_URL)


def get_db() -> Generator[Session, None, None]:
    with db.Session() as session:
        yield session

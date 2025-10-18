from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.dummy import DummyLog
from app.schemas.dummy_schemas import DummyLogCreate


class DummyService:
    def __init__(self, db: Session = Depends(get_db)):
        self._db = db

    def create_dummy_log(self) -> bool:
        try:
            dummy_log = DummyLogCreate(content="Test log")
            self._db.add(dummy_log)
            self._db.commit()
        except Exception:
            self._db.rollback()
            raise
        return True

    def delete_dummy_log(self, db_obj: DummyLog) -> None:
        self._db.delete(db_obj)
        self._db.commit()

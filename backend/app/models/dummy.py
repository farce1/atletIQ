from datetime import datetime
from uuid import UUID as PYTHON_UUID

from sqlalchemy import DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DummyLog(Base):
    __tablename__ = "logs"

    id: Mapped[PYTHON_UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=func.uuid_generate_v4(),
        index=True,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

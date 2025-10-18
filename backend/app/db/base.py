from typing import Any, Iterable

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    id: Any

    def to_dict(
        self,
        columns: Iterable[str] | None = None,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        model_cols = [column.key for column in inspect(self).mapper.column_attrs]
        if not columns:
            columns = model_cols

        if not exclude:
            exclude = []

        return {
            column: getattr(self, column)
            for column in columns
            if column in model_cols and column not in exclude
        }

from pydantic import BaseModel


class DummyLog(BaseModel):
    content: str


class DummyLogCreate(DummyLog):
    pass

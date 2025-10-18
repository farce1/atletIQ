from pydantic import BaseModel


class PongResponse(BaseModel):
    response: str

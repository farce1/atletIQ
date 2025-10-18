from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.api.exceptions.general_exceptions import authentication_failed_error
from app.schemas.response import PongResponse
from app.services.auth import authorise_request

router = APIRouter()


@router.post("/ping")
async def ping(
    request: Request,
    authorised: Annotated[bool, Depends(authorise_request)],
) -> PongResponse:
    if authorised is True:
        return PongResponse(response="pong")
    raise authentication_failed_error()

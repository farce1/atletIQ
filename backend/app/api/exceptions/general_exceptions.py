from fastapi import status

from app.api.exceptions.exceptions_utils import APICustomError
from app.schemas.error_codes import ErrorCode


def authentication_failed_error() -> APICustomError:
    return APICustomError(
        status=status.HTTP_401_UNAUTHORIZED,
        code=ErrorCode.AUTHENTICATION_ERROR,
        message=str("Request authentication failed"),
    )

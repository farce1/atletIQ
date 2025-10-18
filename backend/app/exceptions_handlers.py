from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.exceptions.exceptions_utils import (
    APICustomError,
    APIError,
    APIErrorDetail,
    APIErrorResponse,
    APIMultiValidationError,
    APIValidationError,
)
from app.schemas.error_codes import ErrorCode


def _convert_loc_to_path(loc: tuple[int | str, ...] | None) -> list[str | int]:
    """Convert location tuple to path list, handling None case."""
    return list(loc) if loc is not None else []


def handle_api_custom_error(_: Request, exc: APICustomError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content=jsonable_encoder(
            APIErrorResponse(
                error=APIError(
                    code=exc.code,
                    details=[APIErrorDetail(message=exc.message, path=["_base"])],
                ),
            ),
            exclude_defaults=True,
        ),
    )


def handle_api_validation_error(
    _: Request,
    exc: APIValidationError | APIMultiValidationError,
) -> JSONResponse:
    if isinstance(exc, APIValidationError):
        details = [
            APIErrorDetail(
                code=exc.code,
                message=exc.message,
                path=_convert_loc_to_path(exc.loc),
                ctx=exc.ctx,
            ),
        ]
    else:
        details = [
            APIErrorDetail(
                code=error.code,
                message=error.message,
                path=_convert_loc_to_path(error.loc),
                ctx=error.ctx,
            )
            for error in exc.errors
        ]

    return JSONResponse(
        status_code=exc.status,
        content=jsonable_encoder(
            APIErrorResponse(
                error=APIError(
                    code=ErrorCode.VALIDATION_ERRROR,
                    details=details,
                ),
            ),
        ),
    )


def handle_pydantic_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            APIErrorResponse(
                error=APIError(
                    code=ErrorCode.VALIDATION_ERRROR,
                    details=[
                        APIErrorDetail(
                            code=error["type"],
                            message=error["msg"],
                            path=error["loc"],
                            ctx=error.get("ctx"),
                        )
                        for error in exc.errors()
                    ],
                ),
            ),
        ),
    )


def install_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        APIValidationError,
        handle_api_validation_error,
    )
    app.add_exception_handler(
        APIMultiValidationError,
        handle_api_validation_error,
    )
    app.add_exception_handler(
        RequestValidationError,
        handle_pydantic_validation_error,
    )
    app.add_exception_handler(APICustomError, handle_api_custom_error)

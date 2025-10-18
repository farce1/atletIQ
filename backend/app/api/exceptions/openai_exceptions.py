import openai
from fastapi import status

from app.api.exceptions.exceptions_utils import APICustomError
from app.schemas.error_codes import ErrorCode


def openai_general_error(error: openai.OpenAIError) -> APICustomError:  # noqa: C901
    try:
        raise error
    except openai.APITimeoutError as connectionError:
        return APICustomError(
            status=status.HTTP_504_GATEWAY_TIMEOUT,
            code=ErrorCode.OPENAI_ERROR,
            message=str(
                "OpenAI Error: OpenAI API timeout - repeat the request\n"
                "Raised from OpenAI API response:"
                f"{connectionError.message} -> {connectionError.request}"
            ),
        )
    except openai.InternalServerError as internalError:
        return APICustomError(
            status=status.HTTP_510_NOT_EXTENDED,
            code=ErrorCode.OPENAI_ERROR,
            message=str(
                "OpenAI Error: Internal OpenAI error - repeat the request\n"
                "Raised from OpenAI API response:"
                f"{internalError.message} -> {internalError.request}"
            ),
        )
    except openai.APIConnectionError as connectionError:
        return APICustomError(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code=ErrorCode.OPENAI_ERROR,
            message=str(
                "OpenAI Error: Connection failed - internal fitedo server configuration issue\n"
                "Raised from OpenAI API response:"
                f"{connectionError.message} -> {connectionError.request}"
            ),
        )

    except openai.APIStatusError as generalStatusError:
        if generalStatusError.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            return APICustomError(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                code=ErrorCode.OPENAI_ERROR,
                message=str(
                    "OpenAI Error: Too many requests - check details to handle\n"
                    "Raised from OpenAI API response:"
                    f"{generalStatusError.message} -> {generalStatusError.request}"
                ),
            )
        else:
            return APICustomError(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                code=ErrorCode.OPENAI_ERROR,
                message=str(
                    "OpenAI Error: Connection failed - internal fitedo server issue\n"
                    "Raised from OpenAI API response:"
                    f"{generalStatusError.message} -> {generalStatusError.request}"
                ),
            )

    except (
        openai.AuthenticationError,
        openai.PermissionDeniedError,
    ) as authenticationError:
        return APICustomError(
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
            code=ErrorCode.OPENAI_ERROR,
            message=str(
                "OpenAI Error: Authentication failed - key invalid or permission denied\n"
                "Raised from OpenAI API response:"
                f"{authenticationError.status_code} -> {authenticationError.response}"
            ),
        )

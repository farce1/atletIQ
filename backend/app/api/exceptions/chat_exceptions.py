from fastapi import status

from app.api.exceptions.exceptions_utils import APICustomError
from app.schemas.error_codes import ErrorCode


def session_not_found_error() -> APICustomError:
    return APICustomError(
        status=status.HTTP_404_NOT_FOUND,
        code=ErrorCode.OBJECT_NOT_FOUND,
        message=str("Chat session not found"),
    )


def conversation_not_found_error() -> APICustomError:
    return APICustomError(
        status=status.HTTP_404_NOT_FOUND,
        code=ErrorCode.OBJECT_NOT_FOUND,
        message=str("Chat conversation not found"),
    )


def conversation_already_exists_inactive_error() -> APICustomError:
    return APICustomError(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code=ErrorCode.INACTIVE_SESSION_ACCESSED,
        message=str(
            "Chat conversation archived - provide a new, uniqe conversation key"
        ),
    )


def conversation_already_exists_error() -> APICustomError:
    return APICustomError(
        status=status.HTTP_510_NOT_EXTENDED,
        code=ErrorCode.ACTIVE_SESSION_DROPPED,
        message=str(
            "Chat conversation active but not in context - "
            "resend the request to a new conversation"
        ),
    )


def authentication_failed_error() -> APICustomError:
    return APICustomError(
        status=status.HTTP_401_UNAUTHORIZED,
        code=ErrorCode.AUTHENTICATION_ERROR,
        message=str("Request authentication failed"),
    )


def workflow_timed_out() -> APICustomError:
    return APICustomError(
        status=status.HTTP_504_GATEWAY_TIMEOUT,
        code=ErrorCode.WORKFLOW_TIMED_OUT,
        message=str("Query processing timed out"),
    )


def workflow_runtime_error() -> APICustomError:
    return APICustomError(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code=ErrorCode.WORKFLOW_RUNTIME_ERROR,
        message=str("Error while processing user query"),
    )

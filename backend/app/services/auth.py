from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

api_key_header = APIKeyHeader(name="service-API-key")


def authorise_request(api_key_header: str = Security(api_key_header)) -> bool:
    if api_key_header != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )
    return True

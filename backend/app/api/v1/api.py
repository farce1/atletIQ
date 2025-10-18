from fastapi import APIRouter, Depends

from app.api.v1.endpoints import dummy_endpoint
from app.services.auth import authorise_request

api_router = APIRouter()
api_router.include_router(
    dummy_endpoint.router,
    prefix="/dummy",
    tags=["dummy"],
    dependencies=[Depends(authorise_request)],
)

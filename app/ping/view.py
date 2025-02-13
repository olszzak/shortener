from fastapi import APIRouter

from app.ping.schema import PingResponse
from app.settings import get_settings

router = APIRouter(tags=["ping"])

settings = get_settings()


@router.get("/ping", response_model=PingResponse)
def ping():
    return PingResponse(message="pong")

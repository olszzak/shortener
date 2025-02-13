from http import HTTPStatus
from fastapi.responses import RedirectResponse

from fastapi import APIRouter, Depends, Request

from app.urls.schema import CreateUrlSchema, UrlSchema, StatSchema
from app.urls.service import UrlService, get_urls_service

router = APIRouter(tags=["url"])


@router.post("/urls", response_model=UrlSchema, status_code=HTTPStatus.CREATED)
def add_url(
    url: CreateUrlSchema = Depends(),
    url_service: UrlService = Depends(get_urls_service),
):
    return url_service.create(url)


@router.get("/urls/{url_id}")
def get_url(url_id: str, url_service: UrlService = Depends(get_urls_service)):
    url_obj = url_service.get_url(url_id)

    return RedirectResponse(url_obj.url)


@router.get("/stats/{url_id}", response_model=StatSchema)
def get_url(url_id: str, url_service: UrlService = Depends(get_urls_service)):
    url_obj = url_service.get_by_id(url_id)

    return {
        "url": url_obj.url,
        "count": url_obj.count,
        "created_by_ip": url_obj.created_by_ip,
        "created_by_agent": url_obj.created_by_agent,
    }

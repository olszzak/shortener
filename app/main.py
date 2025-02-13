from http import HTTPStatus
from logging import getLogger

from fastapi import APIRouter, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.ping.view import router as ping_router
from app.urls.view import router as urls_router
from app.settings import get_settings

settings = get_settings()
logger = getLogger(__name__)


def setup_routing(fastapi_app: FastAPI):
    global_router = APIRouter()
    global_router.include_router(ping_router)
    global_router.include_router(urls_router)
    fastapi_app.include_router(global_router)


def setup_exception_handlers(fastapi_app: FastAPI):
    @fastapi_app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        _: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content=jsonable_encoder(exc.detail)
        )

    @fastapi_app.exception_handler(RequestValidationError)
    async def request_validation_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"detail": jsonable_encoder(exc.errors())},
        )

    @fastapi_app.exception_handler(Exception)
    async def unhandled_exceptions_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception(
            f"Unhandled error while processing {request.method} {request.url}",
            exc_info=exc,
        )
        if settings.debug:
            message = str(exc)
        else:
            message = "Internal Server Error"
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content={"detail": message}
        )


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        port=settings.port,
        root_path=settings.api_prefix,
    )
    setup_routing(app)
    setup_exception_handlers(app)
    return app

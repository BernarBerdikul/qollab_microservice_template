import redis
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src import settings
from src.api.v1.api import api_router as api_v1_router
from src.db import cache, dummy_cache, redis_cache  # noqa
from src.middlewares import add_process_time_header
from src.schemas import HealthCheck

app = FastAPI(
    title=settings.app.project_name,
    description=settings.app.description,
    version=settings.app.version,
    # Адрес документации в красивом интерфейсе
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    # Адрес документации в формате OpenAPI
    openapi_url=f"{settings.app.api_doc_prefix}/openapi.json",
    debug=settings.app.debug,
    default_response_class=ORJSONResponse,
)

app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)


# Подключаем роутеры к серверу
app.include_router(router=api_v1_router, prefix="/api/v1")


@app.get("/", response_model=HealthCheck, tags=["status"])
async def health_check():
    return {
        "service": settings.app.project_name,
        "version": settings.app.version,
        "description": settings.app.description,
    }


@app.on_event("startup")
async def startup():
    """Подключаемся к базам при старте сервера"""
    # Redis cache
    cache.cache = redis_cache.RedisCache(
        cache=await redis.asyncio.Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            db=settings.redis.db,
            encoding=settings.redis.encoding,
            max_connections=settings.redis.max_connections,
        ),
    )
    # Fake cache
    # cache.cache = fake_cache.FakeCache()


@app.on_event("shutdown")
async def shutdown():
    """Отключаемся от баз при выключении сервера"""
    await cache.cache.close()


if __name__ == "__main__":
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

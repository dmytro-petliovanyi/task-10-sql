from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from my_app.routers.course_router import course_router
from my_app.routers.group_router import group_router
from my_app.routers.student_router import student_router

app = FastAPI()

app.include_router(group_router)
app.include_router(student_router)
app.include_router(course_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# app/main.py

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.config import Config
from app.routers import api

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include the API router with a prefix, e.g., /api.
app.include_router(api.router, prefix="/api")


@app.on_event("startup")
async def startup():
    # Initialize an async Redis client. Adjust host, port, and db as necessary.
    redis_client = redis.Redis(
        host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

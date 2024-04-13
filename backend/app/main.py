# app/main.py

from fastapi import FastAPI, HTTPException
from .api.v1.routes import api_router
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from limits.storage import RedisStorage
from slowapi.middleware import SlowAPIMiddleware
from redis import Redis, RedisError
import os
import json

REDIS_URL = os.getenv("REDIS_URL")

try:
    limiter = Limiter(key_func=get_remote_address)
    limiter.storage = RedisStorage(REDIS_URL)
except Exception as e:
    print(f"Failed to initialize Redis storage for rate limiter: {e}")

app = FastAPI()

# Make sure you assign the limiter instance to the app's state like this
app.state.limiter = limiter

app.include_router(api_router, prefix="/v1")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add a custom exception handler for rate limit exceeded
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.get("/version")
async def root():
    with open('app/build_info.json') as f:
        data = json.load(f)
    return data

@app.get("/")
async def root():
    return {"message": "If you are seeing this, then the backend is up and running. Please navigate to /docs to see the API documentation."}


@app.get("/test-redis")
async def test_redis_connection():
    redis_url = os.getenv("REDIS_URL")
    try:
        # Initialize a Redis client and attempt to set and get a value
        redis_client = Redis.from_url(redis_url)
        test_key = "test_connection_key"
        test_value = "success"
        redis_client.set(test_key, test_value)
        value = redis_client.get(test_key)
        if value and value.decode("utf-8") == test_value:
            return {"message": "Redis connection and operation successful", "value": value.decode("utf-8")}
        else:
            return {"message": "Redis connection established, but the test operation did not return the expected result."}
    except RedisError as e:
        # If there's an error in the Redis operation, return an error response
        raise HTTPException(status_code=500, detail=f"Redis error: {e}")
    except Exception as e:
        # Catch all other exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
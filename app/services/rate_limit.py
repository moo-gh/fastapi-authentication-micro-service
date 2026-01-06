import time

import redis.asyncio as redis
from fastapi import HTTPException, Request, status

from app.core.config import settings


class RateLimiter:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        # 10 requests per minute for send-code
        self.limit = 10
        self.window = 60

    async def check_rate_limit(self, request: Request, identifier: str):
        key = f"rate_limit:{identifier}"
        current_time = int(time.time())

        async with self.redis_client.pipeline() as pipe:
            # Remove old entries
            await pipe.zremrangebyscore(key, 0, current_time - self.window)
            # Add current request
            await pipe.zadd(key, {str(current_time): current_time})
            # Count requests in window
            await pipe.zcard(key)
            # Set expiry for the key
            await pipe.expire(key, self.window)

            _, _, count, _ = await pipe.execute()

            if count > self.limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests. Please try again later.",
                )


rate_limiter = RateLimiter()


async def rate_limit_dependency(request: Request):
    # Using client IP for rate limiting
    client_ip = request.client.host
    await rate_limiter.check_rate_limit(request, client_ip)

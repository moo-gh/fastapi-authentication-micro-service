import random
import string
import hashlib
from typing import Optional
import redis.asyncio as redis
from app.core.config import settings

class OTPService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    @staticmethod
    def generate_otp(length: int = 6) -> str:
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def hash_otp(otp: str) -> str:
        return hashlib.sha256(otp.encode()).hexdigest()

    async def store_otp(self, project_id: str, email: str, otp: str):
        otp_key = f"otp:{project_id}:{email}"
        attempts_key = f"otp_attempts:{project_id}:{email}"
        hashed_otp = self.hash_otp(otp)
        
        async with self.redis_client.pipeline() as pipe:
            await pipe.set(otp_key, hashed_otp, ex=settings.OTP_EXPIRE_SECONDS)
            await pipe.set(attempts_key, 0, ex=settings.OTP_EXPIRE_SECONDS)
            await pipe.execute()

    async def verify_otp(self, project_id: str, email: str, otp: str) -> bool:
        otp_key = f"otp:{project_id}:{email}"
        attempts_key = f"otp_attempts:{project_id}:{email}"
        
        hashed_otp_stored = await self.redis_client.get(otp_key)
        if not hashed_otp_stored:
            return False

        attempts = await self.redis_client.get(attempts_key)
        if attempts and int(attempts) >= settings.OTP_ATTEMPTS_LIMIT:
            # Too many attempts, expire the OTP early
            await self.redis_client.delete(otp_key)
            return False

        hashed_otp_input = self.hash_otp(otp)
        if hashed_otp_input == hashed_otp_stored:
            # Success, remove the OTP
            await self.redis_client.delete(otp_key)
            await self.redis_client.delete(attempts_key)
            return True
        
        # Increment attempts
        await self.redis_client.incr(attempts_key)
        return False

otp_service = OTPService()



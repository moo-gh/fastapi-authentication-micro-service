from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserService:
    @staticmethod
    async def get_or_create_user(db: AsyncSession, email: str) -> User:
        """
        Gets a user by email or creates a new one if it doesn't exist.
        """
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()

        if not user:
            user = User(email=email)
            db.add(user)
            await db.commit()
            await db.refresh(user)

        return user

    @staticmethod
    async def update_last_verified(db: AsyncSession, user: User) -> None:
        """
        Updates the last_verified_at timestamp for a user.
        """
        user.last_verified_at = datetime.utcnow()
        await db.commit()
        await db.refresh(user)


user_service = UserService()

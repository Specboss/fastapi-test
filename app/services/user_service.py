from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, user_id: int):
        q = await self.db.execute(select(models.User).filter(models.User.id == user_id))
        return q.scalars().first()

    async def get_by_email(self, email: str):
        q = await self.db.execute(select(models.User).filter(models.User.email == email))
        return q.scalars().first()

    async def list_users(self):
        q = await self.db.execute(select(models.User))
        return q.scalars().all()

    async def create_user(self, email: str, hashed_password: str, full_name: str = None, role: str = "user"):
        user = models.User(email=email, hashed_password=hashed_password, full_name=full_name, role=role)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int):
        await self.db.execute(delete(models.User).where(models.User.id == user_id))
        await self.db.commit()

    async def update_user(self, user_id: int, **kwargs):
        await self.db.execute(update(models.User).where(models.User.id == user_id).values(**kwargs))
        await self.db.commit()

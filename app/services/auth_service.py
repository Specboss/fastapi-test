from passlib.context import CryptContext
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    async def authenticate(self, email: str, password: str):
        q = await self.db.execute(select(models.User).filter(models.User.email == email))
        user = q.scalars().first()
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        token = jwt.encode({"sub": str(user.id), "role": user.role.value}, settings.JWT_SECRET,
                           algorithm=settings.JWT_ALGORITHM)
        return token

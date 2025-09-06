from uuid import UUID
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists(self, transaction_id: UUID) -> bool:
        q = await self.db.execute(select(models.Payment).filter(models.Payment.transaction_id == transaction_id))
        return q.scalars().first() is not None

    async def create_payment(self, transaction_id: UUID, account_id: int, user_id: int, amount: Decimal):
        payment = models.Payment(transaction_id=transaction_id, account_id=account_id, user_id=user_id, amount=amount)
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def list_for_user(self, user_id: int):
        q = await self.db.execute(select(models.Payment).filter(models.Payment.user_id == user_id))
        return q.scalars().all()

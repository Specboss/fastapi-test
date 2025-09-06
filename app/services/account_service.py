from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


class AccountService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, account_id: int):
        q = await self.db.execute(select(models.Account).filter(models.Account.id == account_id))
        return q.scalars().first()

    async def get_or_create(self, user_id: int, account_id: int = None):
        if account_id is not None:
            acc = await self.get(account_id)
            if acc:
                return acc
        acc = models.Account(owner_id=user_id, balance=Decimal(0))
        if account_id is not None:
            acc.id = account_id
        self.db.add(acc)
        await self.db.commit()
        await self.db.refresh(acc)
        return acc

    async def list_for_user(self, user_id: int):
        q = await self.db.execute(select(models.Account).filter(models.Account.owner_id == user_id))
        return q.scalars().all()

    async def add_balance(self, account: models.Account, amount):
        account.balance = account.balance + amount
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        return account

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.db import get_session
from app.services.user_service import UserService
from app.services.account_service import AccountService
from app.services.payment_service import PaymentService
from app.schemas import UserRead, AccountRead, PaymentRead
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(payload.get('sub'))
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid token')
    svc = UserService(db)
    user = await svc.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


router = APIRouter()


@router.get('/me', response_model=UserRead)
async def me(user=Depends(get_current_user)):
    return user


@router.get('/accounts', response_model=List[AccountRead])
async def my_accounts(user=Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    svc = AccountService(db)
    return await svc.list_for_user(user.id)


@router.get('/payments', response_model=List[PaymentRead])
async def my_payments(user=Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    svc = PaymentService(db)
    return await svc.list_for_user(user.id)

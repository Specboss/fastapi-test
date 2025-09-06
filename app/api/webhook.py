from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.services.payment_service import PaymentService
from app.services.account_service import AccountService
from app.utils import make_signature

router = APIRouter(prefix='')


@router.post('/webhook/payment')
async def payment_webhook(payload: dict, db: AsyncSession = Depends(get_session)):
    sig = payload.get('signature')
    if not sig:
        raise HTTPException(status_code=400, detail='signature required')
    expected = make_signature(payload)
    if expected != sig:
        raise HTTPException(status_code=400, detail='invalid signature')
    try:
        tid = UUID(payload['transaction_id'])
        user_id = int(payload['user_id'])
        account_id = int(payload['account_id'])
        amount = Decimal(str(payload['amount']))
    except Exception:
        raise HTTPException(status_code=400, detail='invalid payload fields')
    payment_svc = PaymentService(db)
    account_svc = AccountService(db)
    if await payment_svc.exists(tid):
        return {'status': 'already_processed'}
    account = await account_svc.get_or_create(user_id=user_id, account_id=account_id)
    await payment_svc.create_payment(tid, account.id, user_id, amount)
    await account_svc.add_balance(account, amount)
    return {'status': 'ok'}

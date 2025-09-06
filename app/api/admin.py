from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.services.user_service import UserService
from app.services.account_service import AccountService
from app.schemas import UserCreate, UserRead, AccountRead
from app.api.user import get_current_user
from app import models

router = APIRouter(prefix='/admin')


async def admin_required(user=Depends(get_current_user)):
    if user.role != models.Role.admin:
        raise HTTPException(status_code=403, detail='admin only')
    return user


@router.get('/users', response_model=List[UserRead])
async def list_users(admin=Depends(admin_required), db: AsyncSession = Depends(get_session)):
    svc = UserService(db)
    return await svc.list_users()


@router.post('/users', response_model=UserRead)
async def create_user(payload: UserCreate, admin=Depends(admin_required), db: AsyncSession = Depends(get_session)):
    svc = UserService(db)
    from app.services.auth_service import AuthService
    auth_svc = AuthService(db)
    hashed = auth_svc.hash_password(payload.password)
    user = await svc.create_user(payload.email, hashed, payload.full_name, payload.role)
    return user


@router.put('/users/{user_id}')
async def update_user(user_id: int, payload: dict, admin=Depends(admin_required),
                      db: AsyncSession = Depends(get_session)):
    svc = UserService(db)
    await svc.update_user(user_id, **payload)
    return {'status': 'ok'}


@router.patch('/users/{user_id}')
async def patch_user(user_id: int, payload: dict, admin=Depends(admin_required),
                     db: AsyncSession = Depends(get_session)):
    svc = UserService(db)
    await svc.update_user(user_id, **payload)
    return {'status': 'ok'}


@router.delete('/users/{user_id}')
async def delete_user(user_id: int, admin=Depends(admin_required), db: AsyncSession = Depends(get_session)):
    svc = UserService(db)
    await svc.delete_user(user_id)
    return {'status': 'ok'}


@router.get('/users/{user_id}/accounts', response_model=List[AccountRead])
async def user_accounts(user_id: int, admin=Depends(admin_required), db: AsyncSession = Depends(get_session)):
    svc = AccountService(db)
    return await svc.list_for_user(user_id)

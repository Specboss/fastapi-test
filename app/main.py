import asyncio
from fastapi import FastAPI
from sqlalchemy import select

from app.db import engine, Base, AsyncSessionLocal
from app.api import auth as auth, user as user, admin as admin, webhook as webhook
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app import models

app = FastAPI(title='Fastapi-test')

app.include_router(auth.router, prefix='/auth')
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(webhook.router)


@app.on_event('startup')
async def startup():
    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        user_svc = UserService(db)
        existing = await user_svc.get_by_email('user@example.com')
        auth_svc = AuthService(db)
        if not existing:
            hashed = auth_svc.hash_password('userpassword')
            u = await user_svc.create_user('user@example.com', hashed, 'Test User', 'user')
            from app.services.account_service import AccountService
            acc_svc = AccountService(db)
            await acc_svc.get_or_create(user_id=u.id, account_id=1)
        existing_admin = await user_svc.get_by_email('admin@example.com')
        if not existing_admin:
            hashed = auth_svc.hash_password('adminpassword')
            await user_svc.create_user('admin@example.com', hashed, 'Admin User', 'admin')

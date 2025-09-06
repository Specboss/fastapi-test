from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.services.auth_service import AuthService
from app.schemas import Token

router = APIRouter()


class LoginPayload:
    email: str
    password: str


@router.post('/login')
async def login(payload: dict, db: AsyncSession = Depends(get_session)):
    email = payload.get('email')
    password = payload.get('password')
    if not email or not password:
        raise HTTPException(status_code=400, detail='email and password required')
    auth = AuthService(db)
    token = await auth.authenticate(email, password)
    if not token:
        raise HTTPException(status_code=401, detail='invalid credentials')
    return {"access_token": token, "token_type": "bearer"}

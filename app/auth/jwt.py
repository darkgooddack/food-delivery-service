from datetime import datetime, timedelta

from app.auth.security import oauth2_scheme
from app.core.config import settings
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.models.user import User
from app.db.init_db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


def create_tokens(user_id: int):
    access_payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=settings.jwt.access_expire_min)
    }
    refresh_payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=settings.jwt.refresh_expire_days)
    }
    return {
        "access_token": jwt.encode(access_payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm),
        "refresh_token": jwt.encode(refresh_payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm),
        "token_type": "bearer"
    }


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    try:
        payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        user_id: int = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
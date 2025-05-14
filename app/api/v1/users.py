from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.init_db import get_async_session
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.auth.redis import revoke_refresh_token
from app.auth.jwt import get_current_user  # токен в Header


router = APIRouter(prefix="/users", tags=["Auth"])

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    service = UserService(session)
    try:
        return await service.register_user(user.name, user.email, user.password, user.telephone, user.address)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(data: UserLogin, session: AsyncSession = Depends(get_async_session)):
    service = UserService(session)
    result = await service.authenticate_user(data.email, data.password)
    if not result:
        raise HTTPException(status_code=401, detail="Неверные данные")
    tokens, user = result
    return {"user": UserRead.from_orm(user), **tokens}

@router.post("/logout")
async def logout(current_user=Depends(get_current_user)):
    await revoke_refresh_token(current_user.id)
    return {"message": "Вы вышли из системы"}
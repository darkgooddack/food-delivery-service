from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str):
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, name: str, email: str, hashed_password: str, telephone: str, address: str):
        user = User(name=name, email=email, hashed_password=hashed_password, telephone=telephone, address=address)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
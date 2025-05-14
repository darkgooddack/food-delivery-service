from app.repositories.user_repository import UserRepository
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_tokens
from app.auth.redis import store_refresh_token

class UserService:
    def __init__(self, session):
        self.repo = UserRepository(session)

    async def register_user(self, name, email, password, telephone, address):
        if await self.repo.get_by_email(email):
            raise ValueError("Email already exists")
        hashed = hash_password(password)
        return await self.repo.create(name, email, hashed, telephone, address)

    async def authenticate_user(self, email, password):
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None

        tokens = create_tokens(user.id)
        await store_refresh_token(user.id, tokens["refresh_token"])
        return tokens, user
from typing import Optional


from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import User
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService


class UserServiceImpl(UserService):
    def __init__(self, repo=UserRepository()) -> None:
        self.repo = repo

    async def register(
        self,
        user_data: dict,
        session: AsyncSession,
    ) -> int:

        validated_data = self.validate_user_data(user_data)

        if validated_data.get("errors"):
            return validated_data
        user_id = await self.repo.create(validated_data, session)
        return user_id

    async def fetch_users(self, session: AsyncSession) -> list[User]:
        return await self.repo.find_all(session)

    async def fetch_user_info(
        self, user_id: int, session: AsyncSession
    ) -> Optional[User]:
        return await self.repo.find_by_id(user_id, session)

    async def delete_user(self, user_id: int, session: AsyncSession) -> None:
        await self.repo.delete(user_id, session)

    async def update_user(self, user_id: int, data: dict, session: AsyncSession):
        validated_data = self.validate_user_data(data)

        if validated_data.get("errors"):
            return validated_data

        return await self.repo.update(user_id, validated_data, session)

    @staticmethod
    def validate_user_data(data: dict):
        if len(data.get("nickname")) > 50:
            return {"errors": "length of nickname must be less than 50"}
        return data

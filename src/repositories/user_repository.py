from typing import Optional, Union

from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.abstract import AbstractRepository

from core.database.models import User


class UserRepository(AbstractRepository):

    async def create(self, data: dict, session: AsyncSession) -> int:
        q = insert(User).values(data).returning(User.id)
        try:
            user_id = await session.execute(q)
            await session.commit()
            return user_id.scalar()

        except IntegrityError as _:
            return ...

    async def find_by_id(self, entity_id: int, session: AsyncSession) -> Optional[User]:
        q = (
            select(User)
            .where(User.id == entity_id)
            .options(joinedload(User.transactions))
        )
        result = await session.execute(q)
        return result.scalars().unique().one_or_none()

    async def find_all(self, session: AsyncSession) -> list[User]:
        users = await session.execute(
            select(User).options(selectinload(User.transactions))
        )
        return users.scalars().all()

    async def delete(self, entity_id: int, session: AsyncSession) -> None:
        q = delete(User).where(User.id == entity_id)
        await session.execute(q)
        await session.commit()

    async def update(self, entity_id: int, data: dict, session: AsyncSession) -> User:
        q = (
            update(User)
            .where(User.id == entity_id)
            .values(**data)
            .returning(User.nickname, User.id)
        )

        result = await session.execute(q)
        await session.commit()
        await session.flush(result)

        return result.scalars().one()

from typing import Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.database.models import User
from src.repositories.abstract import AbstractRepository


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

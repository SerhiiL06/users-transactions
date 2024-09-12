from src.repositories.abstract import AbstractRepository

from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.models import Transaction, User
from typing import Optional


class TransactionRepository(AbstractRepository):

    async def create(self, data: dict, session: AsyncSession) -> int:

        check_user = await session.execute(
            select(User).where(User.id == data.get("user_id"))
        )

        if check_user.scalars().one_or_none() is None:
            return

        q = insert(Transaction).values(data).returning(Transaction.id)
        result = await session.execute(q)
        await session.commit()
        return result.scalar()

    async def find_all(self, session: AsyncSession, filted_data: dict = None):
        q = (
            select(Transaction)
            .options(joinedload(Transaction.user).load_only(User.nickname))
            .order_by(Transaction.created_at.desc())
        )

        start_date = filted_data.get("start_date")
        end_date = filted_data.get("end_date")

        if start_date:
            q = q.where(Transaction.created_at >= start_date)
        if end_date:
            q = q.where(Transaction.created_at <= end_date)

        result = await session.execute(q)
        return result.scalars().all()

    async def find_by_id(self, entity_id: int, session: AsyncSession):
        q = (
            select(Transaction)
            .where(Transaction.id == entity_id)
            .options(selectinload(Transaction.user))
        )

        result = await session.execute(q)

        return result.scalars().one_or_none()

    def update(self, *args, **kwargs):
        raise NotImplemented()

    def delete(self, *args, **kwargs):
        raise NotImplemented()

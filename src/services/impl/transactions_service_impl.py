from src.services.transactions_service import TransactionService
from typing import Optional, Union

from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.transaction_repository import TransactionRepository

from core.database.models import Transaction, User


class TransactionServiceImpl(TransactionService):

    def __init__(self, repo=TransactionRepository()) -> None:
        self.repo = repo

    async def create_transaction(
        self, user_id: int, amount: int, session: AsyncSession
    ):

        return await self.repo.create({"user_id": user_id, "amount": amount}, session)

    async def get_transactions_list(self, filtered: dict, session: AsyncSession):
        return await self.repo.find_all(session, filtered)

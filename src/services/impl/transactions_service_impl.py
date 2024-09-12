from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.transaction_repository import TransactionRepository
from src.services.transactions_service import TransactionService


class TransactionServiceImpl(TransactionService):

    def __init__(self, repo=TransactionRepository()) -> None:
        self.repo = repo

    async def create_transaction(
        self, user_id: int, amount: int, session: AsyncSession
    ):
        if int(amount) < 1:
            return {"errors": "The amount must be greaten than zero"}

        return await self.repo.create({"user_id": user_id, "amount": amount}, session)

    async def get_transactions_list(self, filtered: dict, session: AsyncSession):
        return await self.repo.find_all(session, filtered)

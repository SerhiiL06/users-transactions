from abc import ABC, abstractmethod


class TransactionService(ABC):

    @abstractmethod
    def create_transaction(self, *args, **kwargs):
        """create user transaction"""

    @abstractmethod
    def get_transactions_list(self, *args, **kwargs):
        """retrieve list of all transactions"""

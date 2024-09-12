from abc import ABC, abstractmethod


class UserService(ABC):

    @abstractmethod
    def register(self):
        """create user entity"""

    @abstractmethod
    def fetch_users(self):
        """get user list"""

    @abstractmethod
    def fetch_user_info(self):
        """retrieve user information with transactions"""

    @abstractmethod
    def delete_user(self):
        """delete user instance"""

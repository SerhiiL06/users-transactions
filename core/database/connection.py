from collections.abc import AsyncGenerator
from typing import Optional
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.settings import settings
from contextlib import asynccontextmanager


class DatabaseCORE:

    def __init__(
        self,
        db_name: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        drivername: str = "sqlite+aiosqlite",
    ) -> None:
        self._DB_NAME = db_name
        self._DB_USERNAME = username
        self._DB_PASSWORD = password
        self._DB_HOST = host
        self._DB_PORT = port
        self.driver = drivername

    @property
    def _db_url(self):
        url = URL.create(
            drivername=self.driver,
            username=self._DB_USERNAME,
            password=self._DB_PASSWORD,
            host=self._DB_HOST,
            port=self._DB_PORT,
            database=self._DB_NAME,
        )
        return url

    @property
    def _engine(self):
        return create_async_engine(self._db_url, echo=True)

    @property
    def session_factory(self) -> async_sessionmaker:
        return async_sessionmaker(self._engine, class_=AsyncSession, autoflush=False)

    async def session_transaction(self) -> AsyncGenerator:
        async with self.session_factory() as conn:
            yield conn


core = DatabaseCORE(settings.database_name)

from collections.abc import AsyncGenerator
from typing import Optional

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.settings import settings


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
        self._db_name = db_name
        self._db_user = username
        self._db_password = password
        self._db_host = host
        self._db_port = port
        self._driver = drivername

    @property
    def _db_url(self):
        url = URL.create(
            drivername=self._driver,
            username=self._db_user,
            password=self._db_password,
            host=self._db_host,
            port=self._db_port,
            database=self._db_name,
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

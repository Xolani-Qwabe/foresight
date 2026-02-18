from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
import logging
from typing import Optional, AsyncGenerator, Generator, Union, Callable

from app.models.db_models.profile import Profile
from app.models.db_models.user import User

logger = logging.getLogger("db_utils")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class DBUtility:
    """
    Utility class for managing database connections and operations (sync and async).
    """

    def __init__(self, engine_url: str, echo: bool = False, async_mode: bool = True):
        """
        Initialize DBUtility.                                                                                                                                                                                                                                                                                                                                                                                                                                 
        :param engine_url: Database connection URL (sync or async)
        :param echo: Whether SQLAlchemy should echo SQL statements
        :param async_mode: If True, uses async engine
        """
        self.engine_url = engine_url
        self.async_mode = async_mode

        if self.async_mode:
            self.engine: Optional[AsyncEngine] = create_async_engine(engine_url, echo=echo)
            self.SessionLocal = sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
        else:
            self.engine = create_engine(engine_url, echo=echo)
            self.SessionLocal = sessionmaker(
                bind=self.engine,
                class_=Session,
                expire_on_commit=False,
            )

        logger.info(f"Initialized {'async' if async_mode else 'sync'} engine for {engine_url}")

    def create_tables(self):
        """
        Create tables synchronously if not in async mode.
        """
        if self.async_mode:
            raise RuntimeError("Use `create_tables_async` for async mode")

        logger.info("Creating tables (sync)...")
        SQLModel.metadata.create_all(self.engine)
        logger.info("Tables created successfully (sync).")

    async def create_tables_async(self):
        """
        Create tables asynchronously if async_mode=True
        """
        if not self.async_mode:
            raise RuntimeError("Use `create_tables` for sync mode")

        logger.info("Creating tables (async)...")
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Tables created successfully (async).")

    def get_db(self) -> Union[Generator[Session, None, None], AsyncGenerator[AsyncSession, None]]:
        """
        Yield a database session depending on async_mode.
        Usage:
        - Sync: `for db in db_util.get_db(): ...`
        - Async: `async for db in db_util.get_db(): ...`
        """
        if self.async_mode:
            async def async_gen() -> AsyncGenerator[AsyncSession, None]:
                async with self.SessionLocal() as session:
                    try:
                        yield session
                    finally:
                        await session.close()
            return async_gen()
        else:
            def sync_gen() -> Generator[Session, None, None]:
                session = self.SessionLocal()
                try:
                    yield session
                finally:
                    session.close()
            return sync_gen()
        
    def get_db_dependency(self) -> Callable:
        """
        Returns a dependency that yields a session for FastAPI routes.
        Usage:
            @app.get("/users")
            def read_users(db=Depends(db_util.get_db_dependency())):
                ...
        Works for both async and sync engines.
        """
        if self.async_mode:
            async def async_dep() -> AsyncGenerator[AsyncSession, None]:
                async with self.SessionLocal() as session:
                    try:
                        yield session
                    finally:
                        await session.close()
            return async_dep
        else:
            def sync_dep() -> Generator[Session, None, None]:
                session = self.SessionLocal()
                try:
                    yield session
                finally:
                    session.close()
            return sync_dep
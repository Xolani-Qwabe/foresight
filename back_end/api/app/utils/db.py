from sqlmodel import SQLModel,Session, create_engine

from sqlalchemy.orm import sessionmaker
import logging
from typing import Generator, Callable

from app.models.db_models.profile import Profile
from app.models.db_models.user import User


logger = logging.getLogger("db_utils")
logger.setLevel(logging.INFO)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class DBUtility:
    """
    Synchronous database utility.
    Uses SQLAlchemy + SQLModel with psycopg2.
    """

    def __init__(self, engine_url: str, echo: bool = False):
        self.engine = create_engine(engine_url, echo=echo)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=Session,
            expire_on_commit=False,
        )

        logger.info(f"Initialized sync engine for {engine_url}")

   
    # Create Tables
    def create_tables(self):
        logger.info("Creating tables (sync)...")
        SQLModel.metadata.create_all(self.engine)
        logger.info("Tables created successfully.")


    # Manual Generator (if needed)
    def get_db(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()


    # FastAPI Dependency
    def get_db_dependency(self) -> Callable:
        def sync_dep() -> Generator[Session, None, None]:
            session = self.SessionLocal()
            try:
                yield session
            finally:
                session.close()

        return sync_dep
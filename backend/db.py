from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from backend.engine import Database

_db: Optional[Database] = None


def init(database_url: str) -> None:
    """
    Initialize the global Database instance once, early in-app startup.
    :param database_url:
    :return:
    """
    global _db
    if _db is None:
        _db = Database(database_url)


async def ping() -> None:
    """
    Ping the db for a callback
    :return:
    """
    if _db is None:
        raise RuntimeError("backend.engine not initialized.")
    await _db.ping()


async def init_models() -> None:
    """
    Initialize all models
    :return:
    """
    if _db is None:
        raise RuntimeError("backend.engine not initialized.")
    await _db.init_models()


@asynccontextmanager
async def session() -> AsyncIterator[AsyncSession]:
    """
    One-liner session usage: 'async with session() as db_session:'
    :return:
    """
    if _db is None:
        raise RuntimeError("backend.engine not initialized.")
    async with _db.get_session() as db_session:
        yield db_session

"""Database utilities for async PostgreSQL connections."""
from typing import AsyncGenerator
from contextlib import asynccontextmanager
import asyncpg
from asyncpg import Pool

from shared.settings import settings


# Global connection pool
_pool: Pool | None = None


async def create_db_pool() -> Pool:
    """Create and return a database connection pool."""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            dsn=settings.database_url.replace("postgresql+asyncpg://", "postgresql://"),
            min_size=2,
            max_size=10,
            command_timeout=60,
        )
    return _pool


async def close_db_pool() -> None:
    """Close the database connection pool."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def get_db_connection():
    """Get a database connection from the pool."""
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        yield connection


@asynccontextmanager
async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """Context manager for database connections."""
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        yield connection

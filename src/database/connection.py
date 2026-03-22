import asyncpg
from asyncpg import Pool

from src.config import settings

_pool: Pool | None = None


async def get_pool() -> Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(settings.database_url)
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def get_db() -> Pool:
    return await get_pool()

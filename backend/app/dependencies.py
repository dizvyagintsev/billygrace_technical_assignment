from functools import lru_cache
from typing import AsyncIterator

import asyncpg
from fastapi import Depends, Request

from app.config import Settings
from app.storage.creatives import Creatives


async def get_db_pool(request: Request) -> AsyncIterator[asyncpg.Pool]:
    pool = request.app.state.db_pool
    try:
        yield pool
    finally:
        pass  # Pool is managed by startup and shutdown events


async def get_creatives_storage(db: asyncpg.Pool = Depends(get_db_pool)) -> Creatives:
    return Creatives(db)


@lru_cache
def get_settings() -> Settings:
    return Settings()

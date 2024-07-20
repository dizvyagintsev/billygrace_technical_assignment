import os
from typing import AsyncGenerator

import asyncpg
import pytest_asyncio

from app.storage.creatives import Creatives


@pytest_asyncio.fixture()
async def creatives_storage() -> AsyncGenerator[Creatives, None]:
    pool = await asyncpg.create_pool(os.environ["POSTGRES_DSN"])
    async with pool.acquire() as connection:
        await connection.set_type_codec(
            "numeric", encoder=str, decoder=float, schema="pg_catalog", format="text"
        )

    yield Creatives(pool)

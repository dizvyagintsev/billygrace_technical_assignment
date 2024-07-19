import os
from typing import Optional

import asyncpg


def dsn_from_env() -> str:
    return "postgresql://postgres:mysecretpassword@localhost:5432/hu"
    return os.environ["POSTGRES_DSN"]


async def create_asyncpg_pool(dsn: Optional[str] = None) -> asyncpg.pool.Pool:
    dsn = dsn or dsn_from_env()

    pool = await asyncpg.create_pool(dsn)
    async with pool.acquire() as connection:
        await connection.set_type_codec(
            "numeric", encoder=str, decoder=float, schema="pg_catalog", format="text"
        )

    return pool

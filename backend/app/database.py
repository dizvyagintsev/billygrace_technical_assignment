import asyncpg

from app.config import Settings


async def create_asyncpg_pool(settings: Settings) -> asyncpg.pool.Pool:
    pool = await asyncpg.create_pool(settings.postgres_dsn)
    async with pool.acquire() as connection:
        await connection.set_type_codec(
            "numeric", encoder=str, decoder=float, schema="pg_catalog", format="text"
        )

    return pool

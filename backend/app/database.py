import asyncpg


async def create_asyncpg_pool(dsn: str) -> asyncpg.pool.Pool:
    pool = await asyncpg.create_pool(dsn)
    async with pool.acquire() as connection:
        await connection.set_type_codec(
            "numeric", encoder=str, decoder=float, schema="pg_catalog", format="text"
        )

    return pool

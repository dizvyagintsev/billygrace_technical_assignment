import pytest_asyncio

from app.database import create_asyncpg_pool
from app.storage.creatives import Creatives


@pytest_asyncio.fixture()
async def creatives_storage():
    yield Creatives(await create_asyncpg_pool())

import os
from typing import AsyncGenerator

import pytest_asyncio

from app.database import create_asyncpg_pool
from app.repository.creatives.creatives import Creatives


@pytest_asyncio.fixture()
async def creatives_storage() -> AsyncGenerator[Creatives, None]:
    yield Creatives(await create_asyncpg_pool(os.environ["POSTGRES_DSN"]))

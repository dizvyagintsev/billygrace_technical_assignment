import os
from pathlib import Path
from typing import AsyncGenerator

import pytest_asyncio
from dotenv import load_dotenv

from app.database import create_asyncpg_pool
from app.repository.creatives.creatives import Creatives

env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(env_path)


@pytest_asyncio.fixture()
async def creatives_repository() -> AsyncGenerator[Creatives, None]:
    dsn = os.getenv("POSTGRES_DSN")

    if not dsn:
        user = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        host = os.environ["POSTGRES_HOST"]
        db = os.environ["POSTGRES_DB"]

        dsn = f"postgresql://{user}:{password}@{host}/{db}"

    yield Creatives(await create_asyncpg_pool(dsn))

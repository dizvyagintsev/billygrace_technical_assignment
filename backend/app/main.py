from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_asyncpg_pool
from app.routers import creatives


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await create_asyncpg_pool()
    yield
    await app.state.db_pool.close()


app = FastAPI(lifespan=lifespan)
app.include_router(creatives.router)

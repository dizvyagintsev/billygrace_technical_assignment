from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database import create_asyncpg_pool
from app.dependencies import get_settings
from app.routers.account.account import router as account_router
from app.routers.creatives.creatives import router as creatives_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.db_pool = await create_asyncpg_pool(get_settings().postgres_dsn)
    yield
    await app.state.db_pool.close()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_router)
app.include_router(creatives_router)

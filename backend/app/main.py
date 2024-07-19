from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database import create_asyncpg_pool
from app.routers import creatives


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await create_asyncpg_pool()
    yield
    await app.state.db_pool.close()


app = FastAPI(lifespan=lifespan)
app.include_router(creatives.router)

origins = [
    "http://localhost:3000",
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

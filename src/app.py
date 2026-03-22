from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import close_pool, get_pool
from src.things.routers.things import router as things_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_pool()
    yield
    await close_pool()


app = FastAPI(title="FastAPI Service", version="0.1.0", lifespan=lifespan)

app.include_router(things_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "fastapi-service"}

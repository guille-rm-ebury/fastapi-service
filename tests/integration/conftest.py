import os

import asyncpg
import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient

from src.app import app
from src.auth.api_key import API_KEY
from src.database import get_db

load_dotenv()

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://user_admin:pass_admin@localhost:5440/fastapi_service_db_test",
)


@pytest.fixture
async def db():
    """Provides a connection with automatic rollback after each test."""
    pool = await asyncpg.create_pool(TEST_DATABASE_URL)
    async with pool.acquire() as conn:
        tx = conn.transaction()
        await tx.start()
        yield conn
        await tx.rollback()
    await pool.close()


@pytest.fixture
async def client(db):
    """HTTP test client with the db dependency overridden."""
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"X-API-Key": API_KEY},
    ) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
async def unauthenticated_client(db):
    """HTTP test client without API key header."""
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

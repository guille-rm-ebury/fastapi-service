from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from src.things.repositories.things_postgres_repository import ThingsPostgresRepository
from src.things.schemas.things import ThingCreate

NOW = datetime(2026, 3, 22, 12, 0, 0, tzinfo=UTC)
THING_ID = UUID("12345678-1234-5678-1234-567812345678")


@pytest.mark.unit
async def test_get_by_id_returns_thing():
    mock_pool = AsyncMock()
    mock_pool.fetchrow.return_value = {
        "id": THING_ID,
        "name": "My Thing",
        "description": "A description",
        "created_at": NOW,
    }
    repo = ThingsPostgresRepository(mock_pool)

    result = await repo.get_by_id(THING_ID)

    assert result.id == THING_ID
    assert result.name == "My Thing"
    mock_pool.fetchrow.assert_awaited_once()


@pytest.mark.unit
async def test_get_by_id_returns_none_when_not_found():
    mock_pool = AsyncMock()
    mock_pool.fetchrow.return_value = None
    repo = ThingsPostgresRepository(mock_pool)

    result = await repo.get_by_id(THING_ID)

    assert result is None


@pytest.mark.unit
async def test_create_returns_thing():
    mock_pool = AsyncMock()
    mock_pool.fetchrow.return_value = {
        "id": THING_ID,
        "name": "Created Thing",
        "description": None,
        "created_at": NOW,
    }
    repo = ThingsPostgresRepository(mock_pool)
    payload = ThingCreate(name="Created Thing")

    result = await repo.create(payload)

    assert result.name == "Created Thing"
    assert result.description is None


@pytest.mark.unit
async def test_delete_returns_true_when_deleted():
    mock_pool = AsyncMock()
    mock_pool.execute.return_value = "DELETE 1"
    repo = ThingsPostgresRepository(mock_pool)

    result = await repo.delete(THING_ID)

    assert result is True


@pytest.mark.unit
async def test_delete_returns_false_when_not_found():
    mock_pool = AsyncMock()
    mock_pool.execute.return_value = "DELETE 0"
    repo = ThingsPostgresRepository(mock_pool)

    result = await repo.delete(THING_ID)

    assert result is False

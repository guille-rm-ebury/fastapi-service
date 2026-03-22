from uuid import UUID

from asyncpg import Pool

from src.database.repository import BaseRepository
from src.things.schemas.things import ThingCreate, ThingRead, ThingUpdate


class ThingsPostgresRepository(BaseRepository[ThingCreate, ThingRead, ThingUpdate]):
    def __init__(self, db: Pool) -> None:
        self._db = db

    async def get_by_id(self, id: UUID) -> ThingRead | None:
        row = await self._db.fetchrow(
            "SELECT id, name, description, created_at FROM things WHERE id = $1",
            id,
        )
        return ThingRead(**dict(row)) if row else None

    async def get_all(self) -> list[ThingRead]:
        rows = await self._db.fetch(
            "SELECT id, name, description, created_at FROM things ORDER BY id"
        )
        return [ThingRead(**dict(row)) for row in rows]

    async def create(self, payload: ThingCreate) -> ThingRead:
        row = await self._db.fetchrow(
            """
            INSERT INTO things (name, description)
            VALUES ($1, $2)
            RETURNING id, name, description, created_at
            """,
            payload.name,
            payload.description,
        )
        return ThingRead(**dict(row))

    async def update(self, id: UUID, payload: ThingUpdate) -> ThingRead | None:
        row = await self._db.fetchrow(
            """
            UPDATE things
            SET
                name = COALESCE($1, name),
                description = COALESCE($2, description)
            WHERE id = $3
            RETURNING id, name, description, created_at
            """,
            payload.name,
            payload.description,
            id,
        )
        return ThingRead(**dict(row)) if row else None

    async def delete(self, id: UUID) -> bool:
        result = await self._db.execute("DELETE FROM things WHERE id = $1", id)
        return result == "DELETE 1"

from uuid import UUID

from src.things.repositories.things_postgres_repository import ThingsPostgresRepository
from src.things.schemas.things import ThingCreate, ThingRead, ThingUpdate


class ThingsService:
    def __init__(self, repository: ThingsPostgresRepository) -> None:
        self._repository = repository

    async def get_all(self) -> list[ThingRead]:
        return await self._repository.get_all()

    async def get_by_id(self, thing_id: UUID) -> ThingRead | None:
        return await self._repository.get_by_id(thing_id)

    async def create(self, payload: ThingCreate) -> ThingRead:
        return await self._repository.create(payload)

    async def update(self, thing_id: UUID, payload: ThingUpdate) -> ThingRead | None:
        return await self._repository.update(thing_id, payload)

    async def delete(self, thing_id: UUID) -> bool:
        return await self._repository.delete(thing_id)

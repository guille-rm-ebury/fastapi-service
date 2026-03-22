from abc import ABC, abstractmethod
from uuid import UUID


class BaseRepository[CreateSchema, ReadSchema, UpdateSchema](ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> ReadSchema | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[ReadSchema]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, payload: CreateSchema) -> ReadSchema:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: UUID, payload: UpdateSchema) -> ReadSchema | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        raise NotImplementedError

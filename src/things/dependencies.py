from asyncpg import Pool
from fastapi import Depends

from src.database import get_db
from src.things.repositories.things_postgres_repository import ThingsPostgresRepository
from src.things.services.things import ThingsService


def get_things_service(db: Pool = Depends(get_db)) -> ThingsService:
    return ThingsService(ThingsPostgresRepository(db))

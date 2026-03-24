from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://user_fastapi:pass_fastapi@fastapi-service-db:5432/fastapi_db"
    cors_allowed_origin: str = "http://localhost:3000"


settings = Settings()

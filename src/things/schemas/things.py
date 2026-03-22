from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Thing(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the thing")
    name: str = Field(..., description="Name of the thing")
    description: str | None = Field(None, description="Optional description of the thing")
    created_at: datetime = Field(..., description="Timestamp when the thing was created")


class ThingCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the thing", examples=["My Thing"])
    description: str | None = Field(None, description="Optional description of the thing", examples=["A useful thing"])


class ThingRead(Thing):
    pass


class ThingUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255, description="New name for the thing", examples=["Updated Name"])
    description: str | None = Field(None, description="New description for the thing", examples=["Updated description"])

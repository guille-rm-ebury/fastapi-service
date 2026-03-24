from pydantic import BaseModel, Field


class InfoRead(BaseModel):
    temperature_celsius: float = Field(description="Current temperature in Madrid in Celsius")
    dog_image_url: str = Field(description="URL of a random dog image")

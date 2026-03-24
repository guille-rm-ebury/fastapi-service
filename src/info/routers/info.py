import asyncio

import httpx
from fastapi import APIRouter

from src.info.schemas.info import InfoRead

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=40.4168&longitude=-3.7038&current=temperature_2m"
)
DOG_URL = "https://dog.ceo/api/breeds/image/random"

router = APIRouter(prefix="/info", tags=["info"])


@router.get(
    "",
    response_model=InfoRead,
    summary="Get combined external info",
    description=(
        "Returns the current temperature in Madrid and a random dog image URL, "
        "fetched concurrently from two public APIs."
    ),
)
async def get_info() -> InfoRead:
    async with httpx.AsyncClient() as client:
        weather_response, dog_response = await asyncio.gather(
            client.get(WEATHER_URL),
            client.get(DOG_URL),
        )

    weather_data = weather_response.json()
    dog_data = dog_response.json()

    return InfoRead(
        temperature_celsius=weather_data["current"]["temperature_2m"],
        dog_image_url=dog_data["message"],
    )

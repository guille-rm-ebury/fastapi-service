from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.info.routers.info import get_info


@pytest.mark.unit
async def test_get_info_returns_combined_data():
    mock_weather_response = MagicMock()
    mock_weather_response.json.return_value = {"current": {"temperature_2m": 18.4}}

    mock_dog_response = MagicMock()
    mock_dog_response.json.return_value = {
        "message": "https://images.dog.ceo/breeds/hound-afghan/n02088094_1003.jpg"
    }

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=[mock_weather_response, mock_dog_response])

    with patch("src.info.routers.info.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=None)

        result = await get_info()

    assert result.temperature_celsius == 18.4
    assert result.dog_image_url == "https://images.dog.ceo/breeds/hound-afghan/n02088094_1003.jpg"


@pytest.mark.unit
async def test_get_info_calls_both_apis_concurrently():
    mock_weather_response = MagicMock()
    mock_weather_response.json.return_value = {"current": {"temperature_2m": 22.1}}

    mock_dog_response = MagicMock()
    mock_dog_response.json.return_value = {
        "message": "https://images.dog.ceo/breeds/labrador/n02099712_100.jpg"
    }

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=[mock_weather_response, mock_dog_response])

    with patch("src.info.routers.info.httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=None)

        result = await get_info()

    assert mock_client.get.await_count == 2
    assert result.temperature_celsius == 22.1
    assert result.dog_image_url == "https://images.dog.ceo/breeds/labrador/n02099712_100.jpg"

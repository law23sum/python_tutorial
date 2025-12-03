"""Weather tools for Pydantic AI agents.

This module provides tools for getting location coordinates and weather information
that can be used by any agent that needs weather capabilities.

This has been adapted from https://ai.pydantic.dev/examples/weather-agent/
"""

from __future__ import annotations as _annotations

from typing import Any

import requests
from httpx import AsyncClient
from pydantic import BaseModel
from pydantic_ai.toolsets import FunctionToolset


class LatLng(BaseModel):
    """Latitude and longitude coordinates."""

    lat: float
    lng: float


async def get_lat_lng(location_description: str) -> LatLng:
    """Get the latitude and longitude of a location.

    Args:
        location_description: A description of a location.
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_description,
        "format": "json",
        "limit": 1,
    }
    headers = {
        "User-Agent": "Example/1.0 (http://0.0.0.0:8000/; cswm7876@yahoo.com)",
        "Referer": "http://0.0.0.0:8000/",
    }
    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()
    if data:
        lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
        return LatLng(lat=lat, lng=lon)
    return LatLng(lat=None, lng=None)


async def get_weather(lat: float, lng: float) -> dict[str, Any]:
    """Get the weather at a location using Open-Meteo API.

    Args:
        lat: Latitude of the location.
        lng: Longitude of the location.
    """
    params = [
        "temperature_2m",
        "precipitation_probability",
        "precipitation",
        "apparent_temperature",
        "weather_code",
        "cloud_cover",
        "rain",
        "showers",
        "visibility",
        "wind_speed_10m",
        "wind_direction_10m",
    ]
    async with AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lng,
                "current": ",".join(params),
            },
        )
        response.raise_for_status()

        data = response.json()
        current = data.get("current", {})
        return current


weather_toolset = FunctionToolset(
    tools=[
        get_lat_lng,
        get_weather,
    ]
)

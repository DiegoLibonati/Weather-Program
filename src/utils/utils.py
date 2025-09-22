from typing import Any

import requests

from src.utils.constants import API_KEY, API_URL


def add_zero(value: int) -> str:
    if value >= 0 and value <= 10:
        return f"0{value}"

    return str(value)


def get_weather_by_location(longitude: float, latitude: float) -> dict[str, Any]:
    if not longitude or not latitude:
        raise ValueError("You must enter a valid longitude and latitude.")

    if not API_KEY:
        raise ValueError(
            "You must enter an API_KEY per submission to be able to query the weather conditions at a specific location."
        )

    url = f"{API_URL}/weather?lat={latitude}&lon={longitude}&appid={API_KEY}"

    response = requests.get(url=url)

    return response.json()

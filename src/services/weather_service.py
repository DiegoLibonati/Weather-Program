from typing import Any

import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from src.core.settings import API_KEY, API_URL


def get_place_information(place: str) -> dict[str, str | float]:
    geolocator = Nominatim(user_agent="weather_program")
    location = geolocator.geocode(place, timeout=10)

    if not location:
        raise ValueError("Location not found.")

    find_timezone = TimezoneFinder()
    timezone = find_timezone.timezone_at(lng=location.longitude, lat=location.latitude)

    return {
        "timezone": timezone,
        "longitude": location.longitude,
        "latitude": location.latitude,
    }


def get_weather_by_location(longitude: float, latitude: float) -> dict[str, Any]:
    if not longitude or not latitude:
        raise ValueError("You must enter a valid longitude and latitude.")

    if not API_KEY:
        raise ValueError("Missing API_KEY for weather request.")

    url = f"{API_URL}/weather?lat={latitude}&lon={longitude}&appid={API_KEY}"
    response = requests.get(url=url)

    return response.json()

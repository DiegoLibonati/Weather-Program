from unittest.mock import MagicMock

import pytest
from pytest import MonkeyPatch

from src.services.weather_service import get_place_information, get_weather_by_location


def test_get_weather_by_location_success(monkeypatch: MonkeyPatch):
    fake_response = {
        "main": {"temp": 280, "feels_like": 278, "humidity": 80, "pressure": 1000},
        "wind": {"speed": 3},
        "weather": [{"description": "cloudy"}],
    }

    mock_get = MagicMock()
    mock_get.json.return_value = fake_response
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_get)

    result = get_weather_by_location(longitude=10, latitude=20)

    assert "main" in result
    assert result["main"]["temp"] == 280


def test_get_weather_by_location_invalid_coordinates():
    with pytest.raises(ValueError):
        get_weather_by_location(longitude=0, latitude=None)


def test_get_place_information_success(monkeypatch: MonkeyPatch):
    mock_location = MagicMock()
    mock_location.longitude = -58.38
    mock_location.latitude = -34.6

    mock_geocode = MagicMock(return_value=mock_location)
    monkeypatch.setattr("src.services.weather_service.Nominatim.geocode", mock_geocode)

    mock_timezone = MagicMock(return_value="America/Argentina/Buenos_Aires")
    monkeypatch.setattr(
        "src.services.weather_service.TimezoneFinder.timezone_at", mock_timezone
    )

    result = get_place_information("Buenos Aires")

    assert result["timezone"] == "America/Argentina/Buenos_Aires"
    assert result["longitude"] == -58.38
    assert result["latitude"] == -34.6


def test_get_place_information_location_not_found(monkeypatch: MonkeyPatch):
    mock_geocode = MagicMock(return_value=None)
    monkeypatch.setattr("src.services.weather_service.Nominatim.geocode", mock_geocode)

    with pytest.raises(ValueError):
        get_place_information("UnknownPlace")

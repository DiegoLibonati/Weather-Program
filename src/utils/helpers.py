from typing import Any


def add_zero(value: int) -> str:
    if value >= 0 and value < 10:
        return f"0{value}"

    return str(value)


def parse_weather_data(data: dict[str, Any]) -> dict[str, int | float | str]:
    kelvinOffset = 273.15

    return {
        "temp": int(data["main"]["temp"] - kelvinOffset),
        "feels_like": int(data["main"]["feels_like"] - kelvinOffset),
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
    }

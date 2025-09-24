from src.utils import add_zero, parse_weather_data


def test_add_zero_with_single_digit():
    assert add_zero(5) == "05"


def test_add_zero_with_two_digits():
    assert add_zero(12) == "12"


def test_parse_weather_data():
    fake_api_response = {
        "main": {
            "temp": 300.15,  # 27 °C
            "feels_like": 303.15,  # 30 °C
            "humidity": 50,
            "pressure": 1013,
        },
        "wind": {"speed": 5},
        "weather": [{"description": "clear sky"}],
    }

    parsed = parse_weather_data(fake_api_response)

    assert parsed["temp"] == 27
    assert parsed["feels_like"] == 30
    assert parsed["wind"] == 5
    assert parsed["description"] == "clear sky"
    assert parsed["humidity"] == 50
    assert parsed["pressure"] == 1013

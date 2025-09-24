import logging
from datetime import datetime
from unittest.mock import patch

import pytest
import pytz

from src.ui.interface_app import InterfaceApp
from src.utils.helpers import add_zero
from src.utils.styles import PRIMARY_COLOR

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def test_initial_config_tk_app(interface_app: InterfaceApp) -> None:
    root = interface_app._root
    root.update()

    title = root.title()
    geometry = root.geometry().split("+")[0]
    resizable = root.resizable()
    config_bg = root.cget("bg")

    assert title == "Weather APP"
    assert geometry == "900x500"
    assert resizable == (False, False)
    assert config_bg == PRIMARY_COLOR


def test_set_datetime(interface_app: InterfaceApp, pytz_timezone: pytz.tzfile) -> None:
    assert not interface_app._label_time.get()

    interface_app._set_datetime(timezone=pytz_timezone)

    time_now_by_timezone = datetime.now(pytz_timezone)
    hours = time_now_by_timezone.hour
    minutes = time_now_by_timezone.minute

    if 12 <= hours <= 23:
        assert (
            interface_app._label_time.get()
            == f"{add_zero(hours)}:{add_zero(minutes)} PM"
        )
    else:
        assert (
            interface_app._label_time.get()
            == f"{add_zero(hours)}:{add_zero(minutes)} AM"
        )


def test_get_weather_success(interface_app: InterfaceApp) -> None:
    interface_app._entry_place.set("Buenos Aires")

    fake_location = {"timezone": "UTC", "longitude": -58.38, "latitude": -34.6}
    fake_weather = {
        "main": {"temp": 300, "feels_like": 298, "humidity": 60, "pressure": 1015},
        "wind": {"speed": 4},
        "weather": [{"description": "sunny"}],
    }

    with patch(
        "src.ui.interface_app.get_place_information", return_value=fake_location
    ), patch("src.ui.interface_app.get_weather_by_location", return_value=fake_weather):
        assert not interface_app._label_current_weather.get()
        assert not interface_app._label_degrees.get()

        interface_app._get_weather()

    assert interface_app._label_current_weather.get() == "CURRENT WEATHER"
    assert interface_app._label_wind_text.get() == "WIND"
    assert interface_app._label_description_text.get() == "DESCRIPTION"
    assert interface_app._label_pressure_text.get() == "PRESSURE"
    assert interface_app._label_humidity_text.get() == "HUMIDITY"

    assert interface_app._label_wind_value.get()
    assert interface_app._label_humidity_value.get()
    assert interface_app._label_pressure_value.get()
    assert interface_app._label_description_value.get()
    assert interface_app._label_thermal_sensation.get()
    assert interface_app._label_degrees.get()


def test_get_weather_invalid_entry(interface_app: InterfaceApp) -> None:
    interface_app._entry_place.set("")

    with pytest.raises(ValueError) as exc_info:
        interface_app._get_weather()

    assert (
        str(exc_info.value) == "You must enter a valid location to check the weather."
    )

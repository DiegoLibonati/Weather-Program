import logging
from datetime import datetime

import pytz

import pytest

from src.models.InterfaceApp import InterfaceApp
from src.utils.utils import add_zero
from src.utils.constants import PRIMARY_COLOR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_initial_config_tk_app(interface_app: InterfaceApp) -> None:
    root = interface_app._root
    root.update()

    title = root.title()
    geometry = root.geometry().split("+")[0]
    resizable = root.resizable()
    config_bg = root.cget("bg")

    assert title == "Wheater APP"
    assert geometry == "900x500"
    assert resizable == (False, False)
    assert config_bg == PRIMARY_COLOR


def test_set_datetime(interface_app: InterfaceApp, pytz_timezone: pytz.tzfile) -> None:
    assert not interface_app._label_time.get()
    
    interface_app._set_datetime(timezone=pytz_timezone)

    time_now_by_timezone = datetime.now(pytz_timezone)

    hours = time_now_by_timezone.hour
    minutes = time_now_by_timezone.minute

    if hours >= 12 and hours <= 23:
        assert interface_app._label_time.get() == f"{add_zero(hours)}:{add_zero(minutes)} PM"
        return
    
    assert interface_app._label_time.get() == f"{add_zero(hours)}:{add_zero(minutes)} AM"


def test_get_place_information(interface_app: InterfaceApp, mock_country: str) -> None:
    information = interface_app._get_place_information(place=mock_country)

    assert information["timezone"]
    assert information["longitude"]
    assert information["latitude"]


def test_get_place_information_invalid_location(interface_app: InterfaceApp) -> None:
    with pytest.raises(ValueError) as exc_info:
        interface_app._get_place_information(place=".,.-{-.}")

    assert str(exc_info.value) == "Location not found."


def test_get_weather_conditions(interface_app: InterfaceApp, mock_coords: dict[str, float]) -> None:
    latitude = mock_coords["latitude"]
    longitude = mock_coords["longitude"]

    weather_conditions = interface_app._get_weather_condtions(latitude=latitude, longitude=longitude)

    assert weather_conditions["temp"]
    assert weather_conditions["feels_like"]
    assert weather_conditions["wind"]
    assert weather_conditions["description"]
    assert weather_conditions["humidity"]
    assert weather_conditions["pressure"]


def test_get_weather_conditions_invalid_coords(interface_app: InterfaceApp) -> None:
    with pytest.raises(ValueError) as exc_info:
        interface_app._get_weather_condtions(longitude="", latitude="")

    assert str(exc_info.value) == "You must enter a valid longitude and latitude."


def test_get_weather(interface_app: InterfaceApp, mock_country: str) -> None:
    interface_app._entry_place.set(mock_country)

    assert not interface_app._label_current_weather.get()
    assert not interface_app._label_wind_text.get()
    assert not interface_app._label_description_text.get()
    assert not interface_app._label_pressure_text.get()
    assert not interface_app._label_humidity_text.get()

    assert not interface_app._label_wind_value.get()
    assert not interface_app._label_humidity_value.get()
    assert not interface_app._label_pressure_value.get()
    assert not interface_app._label_description_value.get()
    assert not interface_app._label_thermal_sensation.get()
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

    assert str(exc_info.value) == "You must enter a valid location to check the weather."
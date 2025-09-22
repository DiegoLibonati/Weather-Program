from test.constants import MOCK_COORDS, MOCK_COUNTRY, MOCK_TIMEZONE
from tkinter import Tk

import pytz
from pytest import fixture

from src.models.InterfaceApp import InterfaceApp


@fixture
def interface_app() -> InterfaceApp:
    root = Tk()
    return InterfaceApp(root=root)


@fixture
def pytz_timezone(mock_timezone: str) -> pytz.tzfile:
    return pytz.timezone(mock_timezone)


@fixture
def mock_timezone() -> str:
    return MOCK_TIMEZONE


@fixture
def mock_country() -> str:
    return MOCK_COUNTRY


@fixture
def mock_coords() -> dict[str, float]:
    return MOCK_COORDS

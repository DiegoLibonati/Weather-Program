from datetime import datetime
from tkinter import Button, Entry, Label, PhotoImage, StringVar, Tk

import pytz

from src.core.paths import PATH_BOX, PATH_LOGO, PATH_SEARCH, PATH_SEARCH_ICON
from src.services.weather_service import get_place_information, get_weather_by_location
from src.utils import add_zero, parse_weather_data
from src.utils.constants import (
    BLACK_COLOR,
    CURSOR_HAND2,
    FONT_POPPINS_15,
    FONT_POPPINS_16,
    FONT_POPPINS_BOLD_25,
    JUSTIFY_CENTER,
    PRIMARY_COLOR,
    RELIEF_FLAT,
    SIDE_BOTTOM,
    WHITE_COLOR,
)


class InterfaceApp:
    def __init__(self, root: Tk, bg: str = PRIMARY_COLOR) -> None:
        self._root = root
        self._root.title("Weather APP")
        self._root.geometry("900x500+300+200")
        self._root.resizable(False, False)
        self._root.config(bg=bg)

        # Imagenes
        self._img_search = PhotoImage(file=PATH_SEARCH)
        self._img_search_icon = PhotoImage(file=PATH_SEARCH_ICON)
        self._img_logo = PhotoImage(file=PATH_LOGO)
        self._img_box = PhotoImage(file=PATH_BOX)

        # Crear widgets
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._entry_place = StringVar()

        # Labels principales
        self._label_current_weather = StringVar()
        self._label_time = StringVar()
        self._label_degrees = StringVar()
        self._label_thermal_sensation = StringVar()

        self._label_wind_text = StringVar()
        self._label_wind_value = StringVar()
        self._label_humidity_text = StringVar()
        self._label_humidity_value = StringVar()
        self._label_description_text = StringVar()
        self._label_description_value = StringVar()
        self._label_pressure_text = StringVar()
        self._label_pressure_value = StringVar()

        # Entrada búsqueda
        Label(image=self._img_search, border=0).place(x=20, y=20)
        Entry(
            bg=WHITE_COLOR,
            width=20,
            font=FONT_POPPINS_BOLD_25,
            fg=PRIMARY_COLOR,
            justify=JUSTIFY_CENTER,
            border=0,
            textvariable=self._entry_place,
        ).place(x=55, y=40)
        Button(
            image=self._img_search_icon,
            border=0,
            bg=WHITE_COLOR,
            width=50,
            height=50,
            relief=RELIEF_FLAT,
            cursor=CURSOR_HAND2,
            command=self._get_weather,
        ).place(x=410, y=32)

        # Logo
        Label(image=self._img_logo, border=0).place(x=150, y=100)

        # Caja inferior
        Label(image=self._img_box, border=0).pack(padx=5, pady=5, side=SIDE_BOTTOM)

        # Labels dinámicos (ejemplo)
        Label(
            font=FONT_POPPINS_15,
            textvariable=self._label_current_weather,
            bg=PRIMARY_COLOR,
            fg=BLACK_COLOR,
        ).place(x=35, y=95)

        Label(
            font=FONT_POPPINS_16,
            textvariable=self._label_time,
            bg=PRIMARY_COLOR,
            fg=BLACK_COLOR,
        ).place(x=35, y=120)

    def _get_weather(self) -> None:
        entry_place_value = self._entry_place.get()
        if not entry_place_value:
            raise ValueError("You must enter a valid location to check the weather.")

        # Labels básicos
        self._label_current_weather.set("CURRENT WEATHER")
        self._label_wind_text.set("WIND")
        self._label_description_text.set("DESCRIPTION")
        self._label_pressure_text.set("PRESSURE")
        self._label_humidity_text.set("HUMIDITY")

        # Info de lugar
        location = get_place_information(entry_place_value)
        timezone = pytz.timezone(location["timezone"])

        # Fecha/hora
        self._set_datetime(timezone=timezone)

        # Clima
        weather_data = get_weather_by_location(
            longitude=round(location["longitude"]),
            latitude=round(location["latitude"]),
        )
        parsed = parse_weather_data(weather_data)

        self._label_wind_value.set(parsed["wind"])
        self._label_humidity_value.set(parsed["humidity"])
        self._label_pressure_value.set(parsed["pressure"])
        self._label_description_value.set(parsed["description"])

        self._label_thermal_sensation.set(
            f"{parsed['description']} | FEELS LIKE {parsed['feels_like']}°"
        )
        self._label_degrees.set(f"{parsed['temp']}°")

    def _set_datetime(self, timezone) -> None:
        time_now_by_timezone = datetime.now(timezone)
        hours = time_now_by_timezone.hour
        minutes = time_now_by_timezone.minute

        suffix = "PM" if 12 <= hours <= 23 else "AM"
        self._label_time.set(f"{add_zero(hours)}:{add_zero(minutes)} {suffix}")

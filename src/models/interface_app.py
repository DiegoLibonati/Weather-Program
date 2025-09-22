from datetime import datetime
from tkinter import Button, Entry, Label, PhotoImage, StringVar, Tk

import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from src.utils.constants import (
    ANCHOR_CENTER,
    BLACK_COLOR,
    CURSOR_HAND2,
    FONT_POPPINS_15,
    FONT_POPPINS_16,
    FONT_POPPINS_20,
    FONT_POPPINS_22,
    FONT_POPPINS_40,
    FONT_POPPINS_BOLD_25,
    JUSTIFY_CENTER,
    PRIMARY_COLOR,
    RELIEF_FLAT,
    SECONDARY_COLOR,
    SIDE_BOTTOM,
    WHITE_COLOR,
)
from src.utils.utils import add_zero, get_weather_by_location


class InterfaceApp:
    def __init__(self, root: Tk, bg: str = PRIMARY_COLOR) -> None:
        # APP Config
        self._root = root
        self._root.title("Wheater APP")
        self._root.geometry("900x500+300+200")
        self._root.resizable(False, False)
        self._root.config(bg=bg)

        self._img_search = PhotoImage(file="./src/assets/search.png")
        self._img_search_icon = PhotoImage(file="./src/assets/search_icon.png")
        self._img_logo = PhotoImage(file="./src/assets/logo.png")
        self._img_box = PhotoImage(file="./src/assets/box.png")

        # Create widges
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._entry_place = StringVar()

        # Labels
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

        # Search

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
            command=lambda: self._get_weather(),
        ).place(x=410, y=32)

        # Logo

        Label(image=self._img_logo, border=0).place(x=150, y=100)

        # Bottom

        Label(image=self._img_box, border=0).pack(padx=5, pady=5, side=SIDE_BOTTOM)

        Label(
            font=FONT_POPPINS_15,
            textvariable=self._label_current_weather,
            bg=PRIMARY_COLOR,
            fg=BLACK_COLOR,
            border=0,
        ).place(x=35, y=95)
        Label(
            font=FONT_POPPINS_16,
            textvariable=self._label_time,
            bg=PRIMARY_COLOR,
            fg=BLACK_COLOR,
            border=0,
        ).place(x=35, y=120)
        Label(
            font=FONT_POPPINS_40,
            textvariable=self._label_degrees,
            bg=PRIMARY_COLOR,
            fg=SECONDARY_COLOR,
            border=0,
        ).place(x=410, y=190)
        Label(
            font=FONT_POPPINS_20,
            textvariable=self._label_thermal_sensation,
            bg=PRIMARY_COLOR,
            fg=SECONDARY_COLOR,
            border=0,
        ).place(x=410, y=250)
        Label(
            font=FONT_POPPINS_20,
            textvariable=self._label_wind_text,
            bg=WHITE_COLOR,
            fg=PRIMARY_COLOR,
            border=0,
        ).place(x=150, y=420, anchor=ANCHOR_CENTER)
        Label(
            font=FONT_POPPINS_22,
            textvariable=self._label_wind_value,
            bg=WHITE_COLOR,
            fg=PRIMARY_COLOR,
            border=0,
        ).place(x=150, y=450, anchor=ANCHOR_CENTER)
        Label(
            font=FONT_POPPINS_20,
            textvariable=self._label_humidity_text,
            bg=WHITE_COLOR,
            fg=PRIMARY_COLOR,
            border=0,
        ).place(x=325, y=420, anchor=ANCHOR_CENTER)
        Label(
            font=FONT_POPPINS_22,
            textvariable=self._label_humidity_value,
            bg=WHITE_COLOR,
            fg=PRIMARY_COLOR,
            border=0,
        ).place(x=325, y=450, anchor=ANCHOR_CENTER)
        Label(
            font=FONT_POPPINS_20,
            textvariable=self._label_description_text,
            bg=WHITE_COLOR,
            fg=PRIMARY_COLOR,
            border=0,
        ).place(x=525, y=420, anchor=ANCHOR_CENTER)
        Label(
            font=FONT_POPPINS_22,
            textvariable=self._label_description_value,
            bg=WHITE_COLOR,
            fg=PRIMARY_COLOR,
            border=0,
        ).place(x=525, y=450, anchor=ANCHOR_CENTER)
        Label(
            font=FONT_POPPINS_20,
            textvariable=self._label_pressure_text,
            bg=WHITE_COLOR,
            fg=PRIMARY_COLOR,
            border=0,
        ).place(x=720, y=420, anchor=ANCHOR_CENTER)
        Label(
            font=FONT_POPPINS_22,
            textvariable=self._label_pressure_value,
            bg=WHITE_COLOR,
            fg=PRIMARY_COLOR,
            border=0,
        ).place(x=720, y=450, anchor=ANCHOR_CENTER)

    def _get_weather(self) -> None:
        entry_place_value = self._entry_place.get()

        if not entry_place_value:
            raise ValueError("You must enter a valid location to check the weather.")

        self._label_current_weather.set("CURRENT WEATHER")
        self._label_wind_text.set("WIND")
        self._label_description_text.set("DESCRIPTION")
        self._label_pressure_text.set("PRESSURE")
        self._label_humidity_text.set("HUMIDITY")

        location = self._get_place_information(place=entry_place_value)

        timezone = pytz.timezone(location["timezone"])
        longitude = location["longitude"]
        latitude = location["latitude"]

        self._set_datetime(timezone=timezone)
        weather_condtions = self._get_weather_condtions(
            latitude=latitude, longitude=longitude
        )

        temp = weather_condtions["temp"]
        feels_like = weather_condtions["feels_like"]
        wind = weather_condtions["wind"]
        description = weather_condtions["description"]
        humidity = weather_condtions["humidity"]
        pressure = weather_condtions["pressure"]

        self._label_wind_value.set(wind)
        self._label_humidity_value.set(humidity)
        self._label_pressure_value.set(pressure)
        self._label_description_value.set(description)

        self._label_thermal_sensation.set(f"{description} | FEELS LIKE {feels_like}°")
        self._label_degrees.set(f"{temp}°")

    def _get_place_information(self, place: str) -> dict[str, str | float]:
        geolocator = Nominatim(user_agent="weather_program")
        location = geolocator.geocode(place, timeout=10)

        if not location:
            raise ValueError("Location not found.")

        find_timezone = TimezoneFinder()
        timezone = find_timezone.timezone_at(
            lng=location.longitude, lat=location.latitude
        )

        return {
            "timezone": timezone,
            "longitude": location.longitude,
            "latitude": location.latitude,
        }

    def _set_datetime(self, timezone: pytz.tzfile) -> None:
        time_now_by_timezone = datetime.now(timezone)

        hours = time_now_by_timezone.hour
        minutes = time_now_by_timezone.minute

        if hours >= 12 and hours <= 23:
            self._label_time.set(f"{add_zero(hours)}:{add_zero(minutes)} PM")
            return

        self._label_time.set(f"{add_zero(hours)}:{add_zero(minutes)} AM")

    def _get_weather_condtions(
        self, longitude: float, latitude: float
    ) -> dict[str, int | float | str]:
        if not longitude or not latitude:
            raise ValueError("You must enter a valid longitude and latitude.")

        data = get_weather_by_location(
            longitude=round(longitude), latitude=round(latitude)
        )

        kelvinOffset = 273.15

        temp = int(data["main"]["temp"] - kelvinOffset)
        feels_like = int(data["main"]["feels_like"] - kelvinOffset)

        wind = data["wind"]["speed"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        return {
            "temp": temp,
            "feels_like": feels_like,
            "wind": wind,
            "description": description,
            "humidity": humidity,
            "pressure": pressure,
        }

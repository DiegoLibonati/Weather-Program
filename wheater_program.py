from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

class Program:

    def __init__(self,master):
        master.title("Wheater APP")
        master.geometry("900x500+300+200")
        master.config(bg="#4c75bd")
        master.resizable(False, False)

        #General
        self.font_family = "poppins"

        # Search
        self.search_image = PhotoImage(file="./search.png")
        self.entry_place = StringVar()
        self.search_icon_image = PhotoImage(file="./search_icon.png")

        Label(image=self.search_image, border=0).place(x=20, y=20)
        Entry(bg="#fff", width=20, font=(self.font_family, 25, "bold"), fg="#4c75bd", justify="center", border=0, textvariable=self.entry_place).place(x=55, y=40)
        Button(image=self.search_icon_image, border=0, bg="#fff", width=50, height=50, relief="flat", cursor="hand2", command=lambda:self.get_Weather()).place(x=410, y=32)

        #Logo

        self.logo_image = PhotoImage(file="./logo.png")
        Label(image=self.logo_image, border=0).place(x=150, y=100)

        #Bottom

        self.box_image = PhotoImage(file="./box.png")
        Label(image=self.box_image, border=0).pack(padx=5, pady=5, side=BOTTOM)

        #Labels
        self.current_weather = StringVar()
        self.time = StringVar()
        self.degrees = StringVar()
        self.thermal_sensation = StringVar()

        self.wind_text = StringVar()
        self.wind_value = StringVar()
        self.humidity_text = StringVar()
        self.humidity_value = StringVar()
        self.description_text = StringVar()
        self.description_value = StringVar()
        self.pressure_text = StringVar()
        self.pressure_value = StringVar()

        Label(font=(self.font_family, 15), textvariable=self.current_weather, bg="#4c75bd", fg="black", border=0).place(x=35,y=95)
        Label(font=(self.font_family, 16), textvariable=self.time, bg="#4c75bd", fg="black", border=0).place(x=35,y=120)
        Label(font=(self.font_family, 40), textvariable=self.degrees, bg="#4c75bd", fg="#F37878", border=0).place(x=410,y=190)
        Label(font=(self.font_family, 20), textvariable=self.thermal_sensation, bg="#4c75bd", fg="#F37878", border=0).place(x=410,y=250)
        Label(font=(self.font_family, 20), textvariable=self.wind_text, bg="white", fg="#4c75bd", border=0).place(x=150,y=420, anchor="center")
        Label(font=(self.font_family, 22), textvariable=self.wind_value, bg="white", fg="#4c75bd", border=0).place(x=150,y=450, anchor="center")
        Label(font=(self.font_family, 20), textvariable=self.humidity_text, bg="white", fg="#4c75bd", border=0).place(x=325,y=420, anchor="center")
        Label(font=(self.font_family, 22), textvariable=self.humidity_value, bg="white", fg="#4c75bd", border=0).place(x=325,y=450, anchor="center")
        Label(font=(self.font_family, 20), textvariable=self.description_text, bg="white", fg="#4c75bd", border=0).place(x=525,y=420, anchor="center")
        Label(font=(self.font_family, 22), textvariable=self.description_value, bg="white", fg="#4c75bd", border=0).place(x=525,y=450, anchor="center")
        Label(font=(self.font_family, 20), textvariable=self.pressure_text, bg="white", fg="#4c75bd", border=0).place(x=720,y=420, anchor="center")
        Label(font=(self.font_family, 22), textvariable=self.pressure_value, bg="white", fg="#4c75bd", border=0).place(x=720,y=450, anchor="center")

    def get_datetime(self, place):
        
        local_time_hours = datetime.now(place).hour
        local_time_minutes = datetime.now(place).minute

        if local_time_hours >= 12 and local_time_hours <= 23:
            return self.time.set(f"{local_time_hours}:{local_time_minutes} PM")
        else: 
            if local_time_hours >= 0 and local_time_hours <10:
                return self.time.set(f"0{local_time_hours}:{local_time_minutes} AM")
            else:
                return self.time.set(f"{local_time_hours}:{local_time_minutes} AM")

    def get_place_location(self, place):

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(place)
        find_time_zone = TimezoneFinder()
        result_time_zone = find_time_zone.timezone_at(lng=location.longitude, lat=location.latitude)

        return [result_time_zone, location.longitude, location.latitude]

    def get_api_info(self, long, lat):

        place_long = long
        place_lat = lat

        API_KEY = 'YOUR API KEY'
        api = f"https://api.openweathermap.org/data/2.5/weather?lat={round(place_lat)}&lon={round(place_long)}&appid={API_KEY}"

        json_data = requests.get(api).json()
        temp = int(json_data["main"]["temp"] - 273.15)
        feels_like = int(json_data["main"]["feels_like"] - 273.15)

        wind = json_data["wind"]["speed"]
        description = json_data["weather"][0]["description"]
        humidity = json_data["main"]["humidity"]
        pressure = json_data["main"]["pressure"]

        return [temp, feels_like, wind, description, humidity, pressure]

    def get_Weather(self):
        self.current_weather.set("CURRENT WEATHER")
        self.wind_text.set("WIND")
        self.description_text.set("DESCRIPTION")
        self.pressure_text.set("PRESSURE")
        self.humidity_text.set("HUMIDITY")
        place = self.entry_place.get()
        
        result_location = self.get_place_location(place)

        result_time_zone = result_location[0]

        entry_place=pytz.timezone(result_time_zone)
        self.get_datetime(entry_place)
        result_api = self.get_api_info(result_location[1], result_location[2])

        self.wind_value.set(result_api[2])
        self.humidity_value.set(result_api[4])
        self.pressure_value.set(result_api[5])
        self.description_value.set(result_api[3])

        self.thermal_sensation.set(f"{result_api[3]} | FEELS LIKE {result_api[1]}°")
        self.degrees.set(f"{result_api[0]}°")





root=Tk()

wheater_app = Program(root)

root.mainloop()

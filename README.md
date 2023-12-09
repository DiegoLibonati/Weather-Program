# Weather-Program

## Getting Started

1. Clone the repository
2. Join to the correct path of the clone
3. Install requirements.txt
4. Use `python wheater_program.py` to execute program

## Description

I made a python program using tkinter as user interface. This program makes requests to a free weather API. We will have to pass the name of the city or country to collect different information. It will show the current weather, the time, the wind chill, the temperature, the wind, the humidity, the description and the pressure.

## Technologies used

1. Python

## Libraries used

1. Tkinter
2. geopy
3. timezonefinder
4. datetime
5. requests
6. pytz

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/28`](https://www.diegolibonati.com.ar/#/project/28)

## Video

https://user-images.githubusercontent.com/99032604/199621088-7b9f342a-5118-4910-b706-8e04ca3e5338.mp4

## Documentation

The `get_datetime()` function gets the current time in hours and minutes of the place we are looking for:

```
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
```

The `get_place_location()` function gets the longitude and latitude of the location you are looking for:

```
def get_place_location(self, place):

    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(place)
    find_time_zone = TimezoneFinder()
    result_time_zone = find_time_zone.timezone_at(lng=location.longitude, lat=location.latitude)

    return [result_time_zone, location.longitude, location.latitude]
```

The `get_api_info()` function obtains the information from the API about the place that was searched, among these we find the temperature, the sensation ends, the wind, the description, the humidity and the pressure:

```
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
```

The `get_Weather()` function grabs the desired location information and renders it to the screen so the user can grab that information:

```
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
```

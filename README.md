# Weather Program

## Getting Started

1. Clone the repository
2. Join to the correct path of the clone
3. Execute: `python -m venv venv`
4. Execute in Windows: `venv\Scripts\activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.test.txt`
7. Use `python -m src.app` to execute program

## Description

I made a python program using tkinter as user interface. This program makes requests to a free weather API. We will have to pass the name of the city or country to collect different information. It will show the current weather, the time, the wind chill, the temperature, the wind, the humidity, the description and the pressure.

## Technologies used

1. Python

## Libraries used

#### Requirements.txt

```
geopy
pytz
requests
timezonefinder
python-dotenv
```

#### Requirements.test.txt

```
pytest
pytest-env
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/Weather-Program`](https://www.diegolibonati.com.ar/#/project/Weather-Program)

## Video

https://user-images.githubusercontent.com/99032604/199621088-7b9f342a-5118-4910-b706-8e04ca3e5338.mp4

## Testing

1. Join to the correct path of the clone
2. Execute in Windows: `venv\Scripts\activate`
3. Execute: `pytest --log-cli-level=INFO`
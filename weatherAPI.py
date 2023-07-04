import requests
import json

OpenWeather_API_KEY = "eac487641a5f879d83763eae5ced0905"


def weatherDataRequest(arrayOfcities):
    cityWeatherHolder = []

    for city in arrayOfcities:
        result = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OpenWeather_API_KEY}"
        ).json()
        # citiesWeatherObject = {
        #     "name": result["name"],
        #     "temp": result["main"]["temp"],
        #     "timezone": result["timezone"],
        # }
        cityWeatherHolder.append(
            [result["name"], result["main"]["temp"], result["timezone"]]
        )

    return cityWeatherHolder

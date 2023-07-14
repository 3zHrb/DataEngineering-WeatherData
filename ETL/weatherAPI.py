import requests
import os
from dotenv import load_dotenv

load_dotenv()


OpenWeather_API_KEY = os.getenv("OpenWeather_API_KEY")


def weatherDataRequest(arrayOfcities):
    cityWeatherHolder = []

    for city in arrayOfcities:
        result = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OpenWeather_API_KEY}"
        ).json()

        cityWeatherHolder.append(
            [
                result["name"],
                result["main"]["temp"],
                result["main"]["humidity"],
                result["timezone"],
            ]
        )

    return cityWeatherHolder

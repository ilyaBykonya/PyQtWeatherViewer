# This Python file uses the following encoding: utf-8
import requests
from typing import Optional
from PySide6 import QtCore
from PySide6 import QtPositioning
from .AbstractLoader import AbstractLoader
from Utils import WeatherInfo, WindInfo

class OpenWeatherLoader(AbstractLoader):
    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key

    def load(self, location: QtPositioning.QGeoCoordinate) -> Optional[WeatherInfo]:
        print(f'Load operation from OpenWeatherLoader [{location.toString()}]')
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={location.latitude()}&lon={location.longitude()}&appid={self.__api_key}').json()
        return self.weather_from_json(response)

    def weather_from_json(self, json) -> Optional[WeatherInfo]:
        try:
            timestamp = QtCore.QDateTime.fromSecsSinceEpoch(int(json['dt']))
            temperature = float(json['main']['temp'])
            coordinate = QtPositioning.QGeoCoordinate(float(json['coord']['lat']), float(json['coord']['lon']))
            clouds = float(json['clouds']['all'])
            wind = WindInfo(float(json['wind']['speed']), float(json['wind']['deg']))
            humidity = float(json['main']['humidity'])
            pressure = float(json['main']['pressure'])
            picture = str(json['weather'][0]['icon'])
            return WeatherInfo(coordinate, timestamp, temperature, clouds, wind, humidity, pressure, picture)
        except:
            pass

        return None













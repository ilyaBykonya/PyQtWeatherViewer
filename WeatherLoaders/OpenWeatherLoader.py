# This Python file uses the following encoding: utf-8
import requests
from typing import Optional
from PySide6 import QtCore
from PySide6 import QtPositioning
from .WeatherInfo import WeatherInfo
from .AbstractLoader import AbstractLoader

class OpenWeatherLoader(AbstractLoader):
    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key

    def load(self, location: QtPositioning.QGeoCoordinate) -> Optional[WeatherInfo]:
        print(f'Load operation from OpenWeatherLoader [{location.toString()}]')
        try:
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={location.latitude()}&lon={location.longitude()}&appid={self.__api_key}').json()
            timestamp = QtCore.QDateTime.fromSecsSinceEpoch(int(response['dt']))
            temperature = float(response['main']['temp'])
            coordinate = QtPositioning.QGeoCoordinate(float(response['coord']['lat']), float(response['coord']['lon']))
            return WeatherInfo(coordinate, timestamp, temperature)
        except:
            pass

        print('On weather loaded [none]')
        return None

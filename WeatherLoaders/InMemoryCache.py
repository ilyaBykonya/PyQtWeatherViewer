# This Python file uses the following encoding: utf-8
from typing import Dict
from typing import Optional
from PySide6 import QtCore
from PySide6 import QtPositioning
from .AbstractLoader import AbstractLoader
from Utils import WeatherInfo, compare_coordinates

class InMemoryCache(AbstractLoader):
    def __init__(self, origin: AbstractLoader, cache_expiration: QtCore.QDateTime) -> None:
        self.__cache: Dict[QtPositioning.QGeoCoordinate, WeatherInfo] = dict()
        self.__cache_expiration: QtCore.QDateTime = cache_expiration
        self.__origin: AbstractLoader = origin

    def load(self, location: QtPositioning.QGeoCoordinate) -> Optional[WeatherInfo]:
        print(f'Load operation from InMemoryCache [{location.toString()}]')
        for coordinate, weather in self.__cache.items():
            if compare_coordinates(coordinate, location):
                if QtCore.QDateTime.currentDateTime().toSecsSinceEpoch() - weather.timestamp.toSecsSinceEpoch() < self.__cache_expiration.toSecsSinceEpoch():
                    return weather
                else:
                    return self.__reload_info(coordinate)

        return self.__reload_info(location)

    def __reload_info(self, location: QtPositioning.QGeoCoordinate) -> WeatherInfo:
        result = self.__origin.load(location)
        if result is not None:
            self.__cache[location] = result
        return result

    def clear(self, location: QtPositioning.QGeoCoordinate) -> None:
        self.__cache = dict((position, weather) for position, weather in self.__cache.items() if not compare_coordinates(position, location))
        self.__origin.clear(location)

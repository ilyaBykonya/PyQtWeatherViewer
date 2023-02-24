# This Python file uses the following encoding: utf-8
from typing import Optional
from PySide6 import QtCore
from PySide6 import QtPositioning
from .AbstractLoader import AbstractLoader
from Utils import WeatherPersistentStorage, WeatherInfo

class CurrentPersistentCache(AbstractLoader):
    def __init__(self, origin: AbstractLoader, cache_expiration: QtCore.QDateTime) -> None:
        self.__cache: WeatherPersistentStorage = WeatherPersistentStorage('./cache/current.ini', cache_expiration)
        self.__origin: AbstractLoader = origin

    def load(self, location: QtPositioning.QGeoCoordinate) -> Optional[WeatherInfo]:
        print(f'Load operation from CurrentPersistentCache [{location.toString()}]')
        from_cache = self.__cache.read(location)
        if from_cache is not None:
            return from_cache
        else:
            return self.__reload_info(location)
    def clear(self, location: QtPositioning.QGeoCoordinate) -> None:
        self.__cache.remove(location)
        self.__origin.clear(location)
    def __reload_info(self, location: QtPositioning.QGeoCoordinate) -> WeatherInfo:
        return self.__cache.upset(location, self.__origin.load(location))

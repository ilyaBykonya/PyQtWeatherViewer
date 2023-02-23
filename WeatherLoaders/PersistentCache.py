# This Python file uses the following encoding: utf-8
from typing import Optional
from PySide6 import QtCore
from PySide6 import QtPositioning
from .WeatherInfo import WeatherInfo
from .WeatherInfo import compare_coordinates
from .AbstractLoader import AbstractLoader

class PersistentCache(AbstractLoader):
    def __init__(self, origin: AbstractLoader, cache_expiration: QtCore.QDateTime) -> None:
        self.__cache: QtCore.QSettings = QtCore.QSettings('./local_cache', QtCore.QSettings.Format.IniFormat)
        self.__cache_expiration: QtCore.QDateTime = cache_expiration
        self.__origin: AbstractLoader = origin

    def __coordinate_to_string(self, location: QtPositioning.QGeoCoordinate) -> str:
        return location.toString()#QtPositioning.QGeoCoordinate.CoordinateFormat.DegreesMinutesSecondsWithHemisphere)

    def load(self, location: QtPositioning.QGeoCoordinate) -> Optional[WeatherInfo]:
        print(f'Load operation from PersistentCache [{location.toString()}]')
        if self.__coordinate_to_string(location) + '/coordinate' in self.__cache.allKeys():
            weather = self.__read_from_cache(location)
            if QtCore.QDateTime.currentDateTime().toSecsSinceEpoch() - weather.timestamp.toSecsSinceEpoch() < self.__cache_expiration.toSecsSinceEpoch():
                return weather
            else:
                return self.__reload_info(location)

        return self.__reload_info(location)

    def clear(self, location: QtPositioning.QGeoCoordinate) -> None:
        self.__remove_from_cache(location)
        self.__origin.clear(location)
    def __reload_info(self, location: QtPositioning.QGeoCoordinate) -> WeatherInfo:
        return self.__write_to_cache(location, self.__origin.load(location))
    def __remove_from_cache(self, location: QtPositioning.QGeoCoordinate) -> None:
        self.__cache.beginGroup(self.__coordinate_to_string(location))
        self.__cache.remove('')
        self.__cache.endGroup()

    def __read_from_cache(self, location: QtPositioning.QGeoCoordinate) -> WeatherInfo:
        self.__cache.beginGroup(self.__coordinate_to_string(location))
        weather = WeatherInfo(
            QtPositioning.QGeoCoordinate(self.__cache.value('coordinate')),
            QtCore.QDateTime(self.__cache.value('timestamp')),
            float(self.__cache.value('temperature')))
        self.__cache.endGroup()
        return weather

    def __write_to_cache(self, location: QtPositioning.QGeoCoordinate, weather: WeatherInfo) -> WeatherInfo:
        if location is None or weather is None:
            return None

        self.__cache.beginGroup(self.__coordinate_to_string(location))
        self.__cache.setValue('coordinate', weather.coordinate)
        self.__cache.setValue('timestamp', weather.timestamp)
        self.__cache.setValue('temperature', weather.temperature)
        self.__cache.endGroup()
        return self.__read_from_cache(location)


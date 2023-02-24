# This Python file uses the following encoding: utf-8
from typing import Optional
from PySide6 import QtCore
from PySide6 import QtPositioning
from .WeatherInfo import WindInfo, WeatherInfo


class WeatherPersistentStorage(QtCore.QObject):
    def __init__(self, filename: str, cache_expiration: QtCore.QDateTime, parent: QtCore.QObject = None) -> None:
        super().__init__(parent)
        self.__storage = QtCore.QSettings(filename, QtCore.QSettings.Format.IniFormat, self)
        self.__cache_expiration: QtCore.QDateTime = cache_expiration

    def __coordinate_to_string(self, location: QtPositioning.QGeoCoordinate) -> str:
        return location.toString()


    def read(self, location: QtPositioning.QGeoCoordinate) -> Optional[WeatherInfo]:
        print(f'Read operation from WeatherPersistentStorage [{location.toString()}]')
        if self.__coordinate_to_string(location) + '/coordinate' in self.__storage.allKeys():
            weather = self.__read_from_cache(location)
            if QtCore.QDateTime.currentDateTime().toSecsSinceEpoch() - weather.timestamp.toSecsSinceEpoch() < self.__cache_expiration.toSecsSinceEpoch():
                return weather
            else:
                self.remove(location)
                return None

    def upset(self, location: QtPositioning.QGeoCoordinate, weather: WeatherInfo) -> WeatherInfo:
        return self.__write_to_cache(location, weather)
    def remove(self, location: QtPositioning.QGeoCoordinate) -> None:
        self.__storage.beginGroup(self.__coordinate_to_string(location))
        self.__storage.remove('')
        self.__storage.endGroup()



    def __read_from_cache(self, location: QtPositioning.QGeoCoordinate) -> WeatherInfo:
        self.__storage.beginGroup(self.__coordinate_to_string(location))

        timestamp = QtCore.QDateTime(self.__storage.value('timestamp'))
        temperature = float(self.__storage.value('temperature'))
        coordinate = QtPositioning.QGeoCoordinate(self.__storage.value('coordinate'))
        clouds = float(self.__storage.value('clouds'))
        wind = WindInfo(float(self.__storage.value('wind/speed')), float(self.__storage.value('wind/direction')))
        himidity = float(self.__storage.value('himidity'))
        pressure = float(self.__storage.value('pressure'))
        weather = WeatherInfo(coordinate, timestamp, temperature, clouds, wind, himidity, pressure)
        self.__storage.endGroup()
        return weather

    def __write_to_cache(self, location: QtPositioning.QGeoCoordinate, weather: WeatherInfo) -> WeatherInfo:
        if location is None or weather is None:
            return None


        self.__storage.beginGroup(self.__coordinate_to_string(location))
        self.__storage.setValue('coordinate', weather.coordinate)
        self.__storage.setValue('timestamp', weather.timestamp)
        self.__storage.setValue('temperature', weather.temperature)
        self.__storage.setValue('clouds', weather.clouds)
        self.__storage.setValue('wind/speed', weather.wind.speed)
        self.__storage.setValue('wind/direction', weather.wind.direction)
        self.__storage.setValue('himidity', weather.himidity)
        self.__storage.setValue('pressure', weather.pressure)
        self.__storage.endGroup()
        return self.__read_from_cache(location)



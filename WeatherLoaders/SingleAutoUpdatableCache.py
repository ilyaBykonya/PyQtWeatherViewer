# This Python file uses the following encoding: utf-8
from typing import Optional
from PySide6 import QtCore, QtPositioning
from Utils import WeatherInfo
from .AbstractLoader import AbstractLoader

class SingleAutoUpdatableCache(QtCore.QObject):
    onValueUpdated = QtCore.Signal()
    def __init__(self, location: QtPositioning.QGeoCoordinate, origin: AbstractLoader, delay: int, parent: QtCore.QObject = None) -> None:
        super().__init__(parent)
        self.__buffer: Optional[WeatherInfo] = None
        self.__location: QtPositioning.QGeoCoordinate = location
        self.__origin: AbstractLoader = origin

        self.__update_timer: QtCore.QTimer = QtCore.QTimer(self)
        self.__update_timer.timeout.connect(self.update_stored_value)
        self.__update_timer.setInterval(delay)
        self.__update_timer.start()


    def update_stored_value(self) -> None:
        self.__reset_internal_buffer(self.__origin.load(self.__location))
    def reset_current_weather(self) -> None:
        self.__origin.clear(self.__location)
        self.update_stored_value()

    def location(self) -> QtPositioning.QGeoCoordinate:
        return self.__location
    def weather(self) -> Optional[WeatherInfo]:
        return self.__buffer
    def __reset_internal_buffer(self, value: Optional[WeatherInfo]) -> None:
        self.__buffer = value
        self.onValueUpdated.emit()


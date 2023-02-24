# This Python file uses the following encoding: utf-8
from typing import Optional
from PySide6 import QtPositioning
from Utils import WeatherInfo

class AbstractLoader():
    def __init__(self) -> None:
        pass
    def load(self, location: QtPositioning.QGeoCoordinate) -> Optional[WeatherInfo]:
        pass
    def clear(self, location: QtPositioning.QGeoCoordinate) -> None:
        pass


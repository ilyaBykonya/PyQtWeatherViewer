# This Python file uses the following encoding: utf-8
from typing import Optional
from PySide6 import QtCore
from PySide6 import QtPositioning

class WindInfo:
    def __init__(self, speed: float, direction: float):
        self.direction: float = direction
        self.speed: float = speed
class WeatherInfo:
    def __init__(self, coordinate: QtPositioning.QGeoCoordinate, timestamp: QtCore.QDateTime, temperature: float, clouds: float, wind: WindInfo, himidity: float, pressure: float):
        self.coordinate: QtPositioning.QGeoCoordinate = coordinate
        self.temperature: float = temperature
        self.timestamp: QtCore.QDateTime = timestamp
        self.clouds: float = clouds
        self.wind: WindInfo = wind
        self.himidity: float = himidity
        self.pressure: float = pressure


def compare_coordinates(left: QtPositioning.QGeoCoordinate, right: QtPositioning.QGeoCoordinate) -> bool:
    return left.distanceTo(right) < 1500#in meters


# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtPositioning

def compare_coordinates(left: QtPositioning.QGeoCoordinate, right: QtPositioning.QGeoCoordinate) -> bool:
    return left.distanceTo(right) < 1500#in meters

class WeatherInfo:
    def __init__(self, coordinate: QtPositioning.QGeoCoordinate, timestamp: QtCore.QDateTime, temperature: float):
        self.coordinate = coordinate
        self.temperature = temperature
        self.timestamp = timestamp

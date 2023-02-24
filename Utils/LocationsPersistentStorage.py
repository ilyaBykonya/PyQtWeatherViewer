# This Python file uses the following encoding: utf-8
from typing import List
from typing import Optional
from PySide6 import QtCore
from PySide6 import QtPositioning


class LocationsPersistentStorage(QtCore.QObject):
    def __init__(self, filename: str, parent: QtCore.QObject = None) -> None:
        super().__init__(parent)
        self.__storage = QtCore.QSettings(filename, QtCore.QSettings.Format.IniFormat, self)

    def insert(self, location: QtPositioning.QGeoCoordinate) -> None:
        current = self.values()
        current.append(location)
        self.__write_locations(current)

    def values(self) -> List[QtPositioning.QGeoCoordinate]:
        return self.__read_locations()

    def remove(self, location: QtPositioning.QGeoCoordinate) -> None:
        current = self.values()
        current.remove(location)
        self.__write_locations(current)

    def __read_locations(self) -> List[QtPositioning.QGeoCoordinate]:
        result: List[QtPositioning.QGeoCoordinate] = list()
        values = self.__storage.value("locations")
        if values is not None:
            for location in values:
                result.append(QtPositioning.QGeoCoordinate(location))
        return result
    def __write_locations(self, locations: List[QtPositioning.QGeoCoordinate]) -> None:
        self.__storage.setValue("locations", locations)




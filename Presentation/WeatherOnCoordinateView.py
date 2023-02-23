# This Python file uses the following encoding: utf-8
from typing import Optional
from PySide6 import QtPositioning, QtWidgets, QtCore
from WeatherLoaders import AbstractLoader, WeatherInfo
from .AutoUpdatableWeatherStorage import AutoUpdatableWeatherStorage

class WeatherOnCoordinateView(QtWidgets.QWidget):
    def __init__(self, location: QtPositioning.QGeoCoordinate, origin: AbstractLoader, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.__storage: AutoUpdatableWeatherStorage = AutoUpdatableWeatherStorage(location, origin, 5000, self)
        self.__storage.onValueUpdated.connect(self.value_updated)

        self.__location_view: QtWidgets.QLabel = QtWidgets.QLabel(location.toString(QtPositioning.QGeoCoordinate.CoordinateFormat.DegreesMinutesSecondsWithHemisphere))
        self.__temperature_view: QtWidgets.QLabel = QtWidgets.QLabel('[no initialized]')

        self.__close_button: QtWidgets.QPushButton = QtWidgets.QPushButton('Close')
        self.__close_button.clicked.connect(self.deleteLater)

        self.__layout = QtWidgets.QHBoxLayout(self)
        self.__layout.addWidget(self.__location_view)
        self.__layout.addWidget(self.__temperature_view)
        self.__layout.addWidget(self.__close_button)



    def value_updated(self):
        weather: WeatherInfo = self.__storage.weather()
        if weather is not None:
            temperature_kelvin = weather.temperature
            temperature_celsium = temperature_kelvin - 273
            self.__temperature_view.setText(f'[{temperature_kelvin}K | {temperature_celsium}C]')
        else:
            self.__temperature_view.setText('[invalid-value]')

# This Python file uses the following encoding: utf-8
from typing import Optional
from PySide6 import QtPositioning, QtWidgets, QtCore
from Utils import WindInfo, WeatherInfo
from WeatherLoaders import AbstractLoader, SingleAutoUpdatableCache

class WeatherOnCoordinateView(QtWidgets.QWidget):
    def __init__(self, location: QtPositioning.QGeoCoordinate, origin: AbstractLoader, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.__storage: SingleAutoUpdatableCache = SingleAutoUpdatableCache(location, origin, 5000, self)
        self.__storage.onValueUpdated.connect(self.value_updated)

        self.__location_view: QtWidgets.QLabel = QtWidgets.QLabel(location.toString(QtPositioning.QGeoCoordinate.CoordinateFormat.DegreesMinutesSecondsWithHemisphere))
        self.__temperature_view: QtWidgets.QLabel = QtWidgets.QLabel('[no initialized]')
        self.__clouds_view: QtWidgets.QLabel = QtWidgets.QLabel('[no initialized]')
        self.__wind_view: QtWidgets.QLabel = QtWidgets.QLabel('[no initialized]')

        self.__close_button: QtWidgets.QPushButton = QtWidgets.QPushButton('Close')
        self.__close_button.clicked.connect(self.deleteLater)

        self.__layout = QtWidgets.QHBoxLayout(self)
        self.__layout.addWidget(self.__location_view,2 )
        self.__layout.addWidget(self.__temperature_view, 2)
        self.__layout.addWidget(self.__clouds_view,2 )
        self.__layout.addWidget(self.__wind_view, 2)
        self.__layout.addWidget(self.__close_button, 1)



    def value_updated(self):
        weather: WeatherInfo = self.__storage.weather()
        if weather is not None:
            self.__temperature_view.setText(f'[{weather.temperature}K | {weather.temperature - 273}C]')
            self.__clouds_view.setText(f'[{weather.clouds}%]')
            self.__wind_view.setText(f'[{weather.wind.direction} | {weather.wind.speed}m/c]')
        else:
            self.__temperature_view.setText('[invalid-value]')
            self.__clouds_view.setText('[invalid-value]')
            self.__wind_view.setText('[invalid-value]')

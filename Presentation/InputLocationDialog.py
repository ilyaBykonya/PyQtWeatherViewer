# This Python file uses the following encoding: utf-8
from typing import Optional
from PySide6 import QtPositioning, QtWidgets, QtCore
from WeatherLoaders import AbstractLoader, WeatherInfo
from .AutoUpdatableWeatherStorage import AutoUpdatableWeatherStorage



class InputLocationDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.setModal(True)

        self.__latitude_selector = QtWidgets.QDoubleSpinBox()
        self.__longitude_selector = QtWidgets.QDoubleSpinBox()
        self.__accept_button = QtWidgets.QPushButton('Ok')
        self.__reject_button = QtWidgets.QPushButton('Cancel')

        self.__latitude_selector.setRange(-90.0, 90.0)
        self.__longitude_selector.setRange(-180.0, 180.0)

        self.__accept_button.clicked.connect(self.accept)
        self.__reject_button.clicked.connect(self.reject)

        self.__window_layout = QtWidgets.QGridLayout(self)
        self.__window_layout.addWidget(QtWidgets.QLabel('Latitude'), 0, 0, 1, 1)
        self.__window_layout.addWidget(QtWidgets.QLabel('Longitude'), 0, 1, 1, 1)
        self.__window_layout.addWidget(self.__latitude_selector, 1, 0, 1, 1)
        self.__window_layout.addWidget(self.__longitude_selector, 1, 1, 1, 1)
        self.__window_layout.addWidget(self.__reject_button, 2, 0, 1, 1)
        self.__window_layout.addWidget(self.__accept_button, 2, 1, 1, 1)

    def coordinate(self) -> QtPositioning.QGeoCoordinate:
        return QtPositioning.QGeoCoordinate(self.__latitude_selector.value(), self.__longitude_selector.value())


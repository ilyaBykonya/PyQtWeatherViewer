# This Python file uses the following encoding: utf-8
import sys
from typing import Optional
from PySide6 import QtPositioning, QtWidgets, QtCore
from Presentation import *
from WeatherLoaders import *

class ApplicationWindow(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)

        loader: AbstractLoader = OpenWeatherLoader('ae53760321911b952e3646887ead8c6d')
        persistent: AbstractLoader = PersistentCache(loader, cache_expiration = QtCore.QDateTime.fromSecsSinceEpoch(10 * 60))#in seconds
        in_memory: AbstractLoader = InMemoryCache(persistent, cache_expiration = QtCore.QDateTime.fromSecsSinceEpoch(5 * 60))#in seconds
        self.__storage: AbstractLoader = in_memory

        self.add_location_button = QtWidgets.QPushButton("Add location");
        self.quit_button = QtWidgets.QPushButton("Close application");
        self.add_location_button.clicked.connect(self.all_observable_location)

        self.__layout = QtWidgets.QVBoxLayout(self)
        self.__layout.addWidget(self.add_location_button, 0, QtCore.Qt.AlignmentFlag.AlignTop)

    def all_observable_location(self):
        input_location_dialog = InputLocationDialog(self)
        if input_location_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            coordinate = input_location_dialog.coordinate()
            weather_view = WeatherOnCoordinateView(coordinate, self.__storage)
            weather_view.destroyed.connect(lambda: self.__remove_location_from_storage(coordinate))
            self.__layout.addWidget(weather_view, 1)

    def __remove_location_from_storage(self, location: QtPositioning.QGeoCoordinate) -> None:
        self.__storage.clear(location)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())

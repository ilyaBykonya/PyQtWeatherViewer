# This Python file uses the following encoding: utf-8
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets


class PictureView(QtWidgets.QLabel):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        self.__picture_name: str = None

    def reset_picture(self, picture_name: str) -> None:
        if self.__picture_name == picture_name:
            return

        self.__picture_name = picture_name
        self.setPixmap(self.pixmap())

    def pixmap(self) -> QtGui.QPixmap:
        return QtGui.QPixmap(f'./resources/pictures/{self.__picture_name}.png')

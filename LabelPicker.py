from PyQt5.QtWidgets import QGridLayout
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class Communication(QObject):
    transfert_position = Signal(int, int)
    pixel_selected = Signal(int, int)
    selecter_leaved = Signal()


class LabelPicker(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent=parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("padding: 0px; ")
        self.messager = Communication()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
          self.messager.pixel_selected.emit(event.pos().x(), event.pos().y())

    def mouseMoveEvent(self, event):
        self.messager.transfert_position.emit(event.pos().x(), event.pos().y())
        if event.buttons() == Qt.LeftButton:
            self.messager.pixel_selected.emit(event.pos().x(), event.pos().y())

    def leaveEvent(self, event):
        self.messager.selecter_leaved.emit()
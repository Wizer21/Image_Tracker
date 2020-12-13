from PyQt5.QtWidgets import QGridLayout
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class Communication(QObject):
    transfert_position = Signal(int, int)
    pixel_selected = Signal(int, int)

class LabelPicker(QLabel):
    def __init__(self, QWidget):
        QLabel.__init__(self)
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)
        self.messager = Communication()

    def mousePressEvent(self, event):
        self.messager.pixel_selected.emit(event.pos().y(), event.pos().x())

    def mouseMoveEvent(self, event):
        self.messager.transfert_position.emit(event.pos().y(), event.pos().x())

    def leaveEvent(self, event):
        print("leaved")
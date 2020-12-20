from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class Webcam_gui(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.main_label = QGridLayout(self)
        self.test_label = QLabel(self)

        self.build()

    def build(self):
        self.setLayout(self.main_label)
        self.main_label.addWidget(self.test_label)
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class Webcam_gui(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.build()

    def build(self):
        print("webcam builded")
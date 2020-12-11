import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PIL import Image


class Trackergui(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    def ini_gui(self):
        self.mainGridLayout = QGridLayout()
        self.containImage = QLabel()
        self.buttonLoad = QPushButton("Load")

        self.setLayout(self.mainGridLayout)

        self.mainGridLayout.addWidget(self.containImage, 0, 0)
        self.mainGridLayout.addWidget(self.buttonLoad, 0, 1)

        self.containImage.setPixmap(QPixmap("greentest.jpg"))

        self.my_image = Image.open("greentest.jpg")
        self.map = self.my_image.load()

        print("-- IMAGE SIZE -- \n" + str(self.my_image.size))
        print("-- IMAGE FIRST PIXEL -- \n" + str(self.map[1,1]))

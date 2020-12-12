from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PIL import Image
from tracker import start_tracker
import time
from Shape import *


class Trackergui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.step = 0
        self.my_color = (0, 0, 0)
        self.map = 0
        self.size = 0
        self.graphic_view = QGraphicsView(self)
        self.timer = QLabel()

    def ini_gui(self):
        self.mainGridLayout = QGridLayout(self)
        self.containImage = QLabel(self)
        self.buttonLoad = QPushButton("Load", self)

        self.setLayout(self.mainGridLayout)

        self.mainGridLayout.addWidget(self.containImage, 0, 0)
        self.mainGridLayout.addWidget(self.buttonLoad, 0, 1)
        self.mainGridLayout.addWidget(self.graphic_view, 1, 0)
        self.mainGridLayout.addWidget(self.timer, 1, 1)

        self.containImage.setPixmap(QPixmap("greentest.jpg"))

        self.my_image = Image.open("greentest.jpg")
        self.map = self.my_image.load()
        self.size = self.my_image.size

        self.step = 5
        self.my_color = (0, 255, 84)

        self.buttonLoad.clicked.connect(self.calltracker)

    @Slot()
    def calltracker(self):
        count = time.time()
        shapes = start_tracker(self.map, self.size, self.step, self.my_color)

        self.polygon = QPolygon()
        self.scene = QGraphicsScene(0, 0, self.size[0], self.size[1])

        for i in range(len(shapes)):
            for j in range(len(shapes[i])):
                for x in range(len(shapes[i].point_cloud)):
                    self.polygon.append(QPoint(shapes[i].point_cloud[x][0], shapes[i].point_cloud[x][1]))

        self.scene.addPolygon(self.polygon)
        self.graphic_view.setScene(self.scene)

        self.timer.setText(str(time.time() - count))

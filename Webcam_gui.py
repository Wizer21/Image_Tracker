from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from numpy import *
from PIL import Image
import cv2
import sys


class Thread(QThread):
    changePixmap = Signal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        fps = cap.get(cv2.CAP_PROP_FPS)  # Print fps
        print("FPS: " + str(fps))
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                image_qt = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(image_qt)

class Webcam_gui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.player_color = 0

        self.main_label = QGridLayout(self)
        self.camera_label = QLabel(self)

        self.color_box = QGroupBox(self)
        self.color_layout = QGridLayout(self)
        self.text_color = QLabel(self)
        self.hover_color = QLabel(self)
        self.min_color = QLabel(self)
        self.mid_color = QLabel(self)
        self.top_color = QLabel(self)

        self.build_ui()
        self.set_up_camera()

    def build_ui(self):
        self.setLayout(self.main_label)
        self.main_label.addWidget(self.camera_label, 0, 0)
        self.main_label.addWidget(self.color_box, 0, 1)
        self.color_box.setLayout(self.color_layout)

        self.color_layout.addWidget(self.text_color, 0, 0, 1, 2)
        self.color_layout.addWidget(self.hover_color, 0, 2)
        self.color_layout.addWidget(self.min_color, 1, 0)
        self.color_layout.addWidget(self.mid_color, 1, 1)
        self.color_layout.addWidget(self.top_color, 1, 2)

        self.hover_color.setText("hovcolor")  # TEMPORAIRE TEST
        self.min_color.setText("min")
        self.mid_color.setText("mid")
        self.top_color.setText("top")

        self.color_layout.setAlignment(Qt.AlignTop)
        self.color_box.setTitle("Color")
        self.text_color.setText("Hovered")

    def set_up_camera(self):
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    @Slot(QImage)
    def setImage(self, image):
        self.camera_label.setPixmap(QPixmap.fromImage(image))

        color = QColor(image.pixel(0, 0))
        test = color.red()
        test1 = color.blue()
        test2 = color.green()
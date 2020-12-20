from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Image_gui import *
from Webcam_gui import *


class Main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.main_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self)

        self.menu_bar = QMenuBar(self)
        self.media_menu = QMenu(self)
        self.image_action = QAction(self)
        self.webcam_action = QAction(self)

        self.stack = QStackedWidget(self)
        self.image_gui = Image_gui()
        self.webcam_gui = Webcam_gui()

        self.build()

    def build(self):
        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.addWidget(self.stack)

        self.stack.addWidget(self.image_gui)
        self.stack.addWidget(self.webcam_gui)
        self.stack.setCurrentIndex(0)

        self.setMenuBar(self.menu_bar)
        self.menu_bar.addMenu(self.media_menu)
        self.media_menu.addAction(self.image_action)
        self.media_menu.addAction(self.webcam_action)

        self.image_action.triggered.connect(self.set_at_image)
        self.webcam_action.triggered.connect(self.set_at_webcam)

    @Slot()
    def set_at_image(self):
        self.stack.setCurrentIndex(0)

    @Slot()
    def set_at_webcam(self):
        self.stack.setCurrentIndex(1)
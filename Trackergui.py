from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PIL import Image
from tracker import start_tracker
import time
from Shape import *
from LabelPicker import *

class Trackergui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.step = 0
        self.my_color = (0, 0, 0)
        self.map = 0
        self.size = 0
        self.step = 2
        self.are_dynamic_settings = False
        self.min_color = (0, 255, 84)
        self.my_color = (0, 255, 84)
        self.max_color = (0, 255, 84)
        self.color_range = 0
        self.looking_for_new_color = False

        self.mainGridLayout = QGridLayout(self)
        self.containImage = LabelPicker(self)
        self.graphic_view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)

        self.settingswidget = QWidget(self)
        self.settingslayout = QGridLayout(self)

        self.label_dynamicset = QLabel(self)
        self.box_isdynamic = QCheckBox(self)

        self.widget_step = QWidget(self)
        self.layout_step = QGridLayout(self)
        self.title_step = QLabel(self)
        self.value_step = QLabel(self)
        self.scroll_step = QSlider(self)

        self.widget_color = QWidget(self)
        self.layout_color = QGridLayout(self)
        self.title_color = QLabel(self)
        self.dynamic_color_label = QLabel(self)
        self.display_mincolor = QLabel(self)
        self.display_currentcolor = QLabel(self)
        self.display_maxcolor = QLabel(self)
        self.scroll_color = QSlider(self)

        self.timer = QLabel(self)
        self.buttonLoad = QPushButton(self)

    def ini_gui(self):

        #  Build Main
        self.setLayout(self.mainGridLayout)

        self.mainGridLayout.addWidget(self.containImage, 0, 0)
        self.mainGridLayout.addWidget(self.graphic_view, 1, 0)
        self.mainGridLayout.addWidget(self.settingswidget, 0, 1, 2, 1)

        # Build Settings
        self.settingswidget.setLayout(self.settingslayout)

        self.settingslayout.addWidget(self.label_dynamicset, 0, 0)
        self.settingslayout.addWidget(self.box_isdynamic, 0, 1)

        self.settingslayout.addWidget(self.widget_step, 1, 0, 1, 2)  # STEP
        self.widget_step.setLayout(self.layout_step)
        self.layout_step.addWidget(self.title_step, 0, 0)
        self.layout_step.addWidget(self.value_step, 0, 1)
        self.layout_step.addWidget(self.scroll_step, 1, 0, 1, 2)

        self.settingslayout.addWidget(self.widget_color, 2, 0, 1, 2)  # COLOR
        self.widget_color.setLayout(self.layout_color)
        self.layout_color.addWidget(self.title_color, 0, 0)
        self.layout_color.addWidget(self.dynamic_color_label, 0, 2)
        self.layout_color.addWidget(self.display_mincolor, 1, 0)
        self.layout_color.addWidget(self.display_currentcolor, 1, 1)
        self.layout_color.addWidget(self.display_maxcolor, 1, 2)
        self.layout_color.addWidget(self.scroll_color, 2, 0, 1, 3)

        self.settingslayout.addWidget(self.timer, 3, 0, 1, 2)
        self.settingslayout.addWidget(self.buttonLoad, 4, 0, 1, 2)

        # Complete Settings
        self.label_dynamicset.setText("Dynamic Settings")

        self.title_step.setText("Step")
        self.value_step.setText("2")
        self.scroll_step.setOrientation(Qt.Horizontal)
        self.scroll_step.setRange(2, 40)
        self.scroll_step.setValue(2)
        self.scroll_step.setPageStep(1)
        self.scroll_step.setCursor(Qt.PointingHandCursor)

        self.title_color.setText("Color")
        self.dynamic_color_label.setText("main")
        self.display_mincolor.setText("min")
        self.display_currentcolor.setText("mid")
        self.display_maxcolor.setText("top")
        self.scroll_color.setOrientation(Qt.Horizontal)
        self.scroll_color.setCursor(Qt.PointingHandCursor)

        self.timer.setText("0")
        self.buttonLoad.setText("Load")
        self.buttonLoad.setCursor(Qt.PointingHandCursor)

        self.settingslayout.setAlignment(Qt.AlignTop)

        self.apply_new_color(self.my_color)

        # Build
        self.containImage.setPixmap(QPixmap("greentest.jpg"))

        self.my_image = Image.open("greentest.jpg")
        self.map = self.my_image.load()
        self.size = self.my_image.size
        self.containImage.setFixedSize(self.size[0], self.size[1])

        self.box_isdynamic.stateChanged.connect(self.new_state)
        self.scroll_step.valueChanged.connect(self.step_changed)
        self.scroll_color.valueChanged.connect(self.new_range_color)
        self.buttonLoad.clicked.connect(self.calltracker)

        self.containImage.messager.pixel_selected.connect(self.apply_newpixel_selected)
        self.containImage.messager.transfert_position.connect(self.display_temporary_color)
        self.containImage.messager.selecter_leaved.connect(self.apply_selecter_leaved)

    @Slot()
    def calltracker(self):
        count = time.time()
        shapes = start_tracker(self.map, self.size, self.step, self.min_color, self.max_color)

        self.polygon = QPolygon()
        self.scene.setSceneRect(0, 0, self.size[0], self.size[1])
        self.scene.clear()

        color_pen = QPen(Qt.red)

        self.scene.addPixmap(QPixmap("testtrackerlow.jpg"))

        for i in range(len(shapes)):
            self.polygon.clear()
            for j in range(len(shapes[i].point_cloud)):
                self.polygon.append(QPoint(shapes[i].point_cloud[j][0], shapes[i].point_cloud[j][1]))
            self.scene.addRect(QRect(shapes[i].top_left[0], shapes[i].top_left[1], shapes[i].width, shapes[i].height), color_pen)
            self.scene.addPolygon(self.polygon)

        self.graphic_view.setScene(self.scene)

        self.timer.setText(str(time.time() - count))

    @Slot(int)
    def step_changed(self, value):
        self.value_step.setText(str(value))
        self.step = value
        if self.are_dynamic_settings:
            self.calltracker()

    @Slot(int)
    def new_state(self, position):
        if position == 0:
            self.are_dynamic_settings = False
        if position == 2:
            self.are_dynamic_settings = True

    @Slot(int)
    def new_range_color(self, value):
        self.color_range = value
        self.apply_new_color(self.my_color)
        if self.are_dynamic_settings:
            self.calltracker()

    def apply_new_color(self, newcolor):
        pix_color = QPixmap(50, 50)
        pix_color.fill(QColor(newcolor[0], newcolor[1], newcolor[2]))

        self.my_color = newcolor
        self.display_currentcolor.setPixmap(pix_color)

        # Set Min Color
        rgb_color = [self.my_color[0], self.my_color[1], self.my_color[2]]
        for i in range(len(rgb_color)):
            rgb_color[i] -= self.color_range
            if rgb_color[i] < 0:
                rgb_color[i] = 0

        self.min_color = (rgb_color[0], rgb_color[1], rgb_color[2])
        pix_color.fill(QColor(self.min_color[0], self.min_color[1], self.min_color[2]))
        self.display_mincolor.setPixmap(pix_color)

        # Set Max Color
        rgb_color = [self.my_color[0], self.my_color[1], self.my_color[2]]
        for i in range(len(rgb_color)):
            rgb_color[i] += self.color_range
            if 255 < rgb_color[i]:
                rgb_color[i] = 255

        self.max_color = (rgb_color[0], rgb_color[1], rgb_color[2])
        pix_color.fill(QColor(self.max_color[0], self.max_color[1], self.max_color[2]))
        self.display_maxcolor.setPixmap(pix_color)

    @Slot(int, int)
    def display_temporary_color(self, y, x):
        color_in_pixmap = QPixmap(50, 50)
        pixel = self.map[y, x]

        color_in_pixmap.fill(QColor(pixel[0], pixel[1], pixel[2]))
        self.dynamic_color_label.setPixmap(color_in_pixmap)

    @Slot(int, int)
    def apply_newpixel_selected(self, y, x):
        self.apply_new_color(self.map[y, x])

    @Slot()
    def apply_selecter_leaved(self):
        color_pix = QPixmap(50, 50)
        color_pix.fill(Qt.transparent)
        self.dynamic_color_label.setPixmap(color_pix)

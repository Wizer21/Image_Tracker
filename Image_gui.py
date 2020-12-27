from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PIL import Image
from tracker import start_tracker
import time
from Shape import *
from LabelPicker import *


class Image_gui(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.step = 0
        self.my_color = (0, 0, 0)
        self.map = 0
        self.size = 0
        self.step = 2
        self.compiler_value = 0
        self.are_dynamic_settings = False
        self.min_color = (0, 255, 84)
        self.my_color = (0, 255, 84)
        self.max_color = (0, 255, 84)
        self.color_range = 0
        self.looking_for_new_color = False
        self.image_url = ".\\files\\banana.jpg"
        self.low_pixmap = QPixmap()

        self.mainGridLayout = QGridLayout(self)

        self.containImage = LabelPicker(self)  # GRAPH
        self.graphic_view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.point_visibles = True
        self.rect_visibles = True
        self.middle_visible = True
        self.shapes = []

        self.settingswidget = QWidget(self)
        self.borderlayout = QGridLayout(self)

        self.button_new_file = QPushButton("New File", self)

        self.settigns_box = QGroupBox("Settings", self)  # SETTINGS
        self.settingslayout = QGridLayout(self)

        self.widget_step = QWidget(self)  # STEP
        self.layout_step = QGridLayout(self)
        self.title_step = QLabel("Step", self)
        self.value_step = QLabel("2", self)
        self.scroll_step = QSlider(self)
        self.combine_shapes = QLabel("Combine shapes", self)
        self.scroll_combine = QSlider(self)
        self.display_combine_range = QLabel("Off", self)

        self.widget_color = QWidget(self)  # COLOR
        self.layout_color = QGridLayout(self)
        self.title_color = QLabel("Color", self)
        self.dynamic_color_label = QLabel(self)
        self.display_mincolor = QLabel(self)
        self.display_currentcolor = QLabel(self)
        self.display_maxcolor = QLabel(self)
        self.scroll_color = QSlider(self)

        self.box_build = QGroupBox("Build", self)  # BUILD
        self.grid_build = QGridLayout(self)
        self.display_calctime = QLabel("0", self)
        self.calctime = QLabel("Calc time", self)
        self.graph_sec = QLabel("Display time", self)
        self.display_graph_sec = QLabel("0", self)
        self.display_nbr_item = QLabel("0", self)
        self.nbr_item = QLabel("Items found", self)

        self.buttonLoad = QPushButton("Load", self)  # LOAD
        self.quick_load = QLabel("Dynamic load", self)
        self.box_isdynamic = QCheckBox(self)

        self.graphic_box = QGroupBox("Graphic", self)  # GRAPHIC
        self.layout_graph = QGridLayout(self)
        self.points = QLabel("Points", self)
        self.point_box = QCheckBox(self)
        self.square = QLabel("Square", self)
        self.square_box = QCheckBox(self)
        self.center = QLabel("Center", self)
        self.center_box = QCheckBox(self)

        self.ini_gui()

    def ini_gui(self):
        #  Build Main
        self.setLayout(self.mainGridLayout)
        self.load_image()

        self.mainGridLayout.addWidget(self.graphic_view, 1, 0)
        self.mainGridLayout.addWidget(self.settingswidget, 0, 1, 2, 1)

        #  IMAGES
        self.mainGridLayout.addWidget(self.containImage, 0, 0)
        self.load_image()

        # Build Settings
        self.settingswidget.setLayout(self.borderlayout)

        self.borderlayout.addWidget(self.button_new_file, 0, 0, 1, 2)  # NEW FILE

        self.borderlayout.addWidget(self.settigns_box, 1, 0, 1, 2)  # BOX
        self.settigns_box.setLayout(self.settingslayout)

        self.settingslayout.addWidget(self.widget_step, 1, 0)  # STEP
        self.widget_step.setLayout(self.layout_step)
        self.layout_step.addWidget(self.title_step, 0, 0)
        self.layout_step.addWidget(self.value_step, 0, 1)
        self.layout_step.addWidget(self.scroll_step, 1, 0, 1, 2)
        self.layout_step.addWidget(self.combine_shapes, 2, 0, 1, 2)
        self.layout_step.addWidget(self.scroll_combine, 3, 0)
        self.layout_step.addWidget(self.display_combine_range, 3, 1)

        self.settingslayout.addWidget(self.widget_color, 2, 0)  # COLOR
        self.widget_color.setLayout(self.layout_color)
        self.layout_color.addWidget(self.title_color, 0, 0)
        self.layout_color.addWidget(self.dynamic_color_label, 0, 2)
        self.layout_color.addWidget(self.display_mincolor, 1, 0, Qt.AlignRight)
        self.layout_color.addWidget(self.display_currentcolor, 1, 1)
        self.layout_color.addWidget(self.display_maxcolor, 1, 2, Qt.AlignLeft)
        self.layout_color.addWidget(self.scroll_color, 2, 0, 1, 3)

        self.borderlayout.addWidget(self.box_build, 2, 0, 1, 2)  # BUILD
        self.box_build.setLayout(self.grid_build)
        self.grid_build.addWidget(self.calctime, 0, 0)
        self.grid_build.addWidget(self.display_calctime, 1, 0)
        self.grid_build.addWidget(self.graph_sec, 2, 0)
        self.grid_build.addWidget(self.display_graph_sec, 3, 0)
        self.grid_build.addWidget(self.nbr_item, 4, 0)
        self.grid_build.addWidget(self.display_nbr_item, 5, 0)

        self.borderlayout.addWidget(self.buttonLoad, 3, 0, 1, 2)  # LOAD
        self.borderlayout.addWidget(self.box_isdynamic, 4, 0)
        self.borderlayout.addWidget(self.quick_load, 4, 1)
        self.borderlayout.setColumnStretch(0, 0)
        self.borderlayout.setColumnStretch(1, 1)

        self.borderlayout.addWidget(self.graphic_box, 5, 0, 1, 2)
        self.graphic_box.setLayout(self.layout_graph)
        self.layout_graph.addWidget(self.point_box, 0, 0)
        self.layout_graph.addWidget(self.points, 0, 1)
        self.layout_graph.addWidget(self.square_box, 1, 0)
        self.layout_graph.addWidget(self.square, 1, 1)
        self.layout_graph.addWidget(self.center_box, 2, 0)
        self.layout_graph.addWidget(self.center, 2, 1)
        self.layout_graph.setColumnStretch(0, 0)
        self.layout_graph.setColumnStretch(1, 1)

        # Complete Settings
        self.button_new_file.setCursor(Qt.PointingHandCursor)
        self.button_new_file.setIcon(QPixmap(".\\files\\newfile.png"))

        self.scroll_step.setOrientation(Qt.Horizontal)  # STEP
        self.scroll_step.setRange(2, 40)
        self.scroll_step.setValue(2)
        self.scroll_step.setPageStep(1)
        self.scroll_step.setCursor(Qt.PointingHandCursor)
        self.scroll_combine.setOrientation(Qt.Horizontal)
        self.scroll_combine.setRange(0, 50)
        self.scroll_combine.setValue(0)
        self.scroll_combine.setPageStep(1)
        self.scroll_combine.setCursor(Qt.PointingHandCursor)

        self.dynamic_color_label.setFixedSize(80, 40)  # COLOR
        self.display_mincolor.setFixedSize(80, 40)
        self.display_currentcolor.setFixedSize(80, 40)
        self.display_maxcolor.setFixedSize(80, 40)
        self.layout_color.setContentsMargins(0, 0, 0, 0)
        self.scroll_color.setOrientation(Qt.Horizontal)
        self.scroll_color.setCursor(Qt.PointingHandCursor)

        self.buttonLoad.setCursor(Qt.PointingHandCursor)  # LOAD
        self.box_isdynamic.setCursor(Qt.PointingHandCursor)
        self.buttonLoad.setIcon(QPixmap(".\\files\\quickload.png"))

        self.borderlayout.setAlignment(Qt.AlignTop)

        self.point_box.setChecked(True)  # GRAPHIC
        self.square_box.setChecked(True)
        self.center_box.setChecked(True)
        self.point_box.setCursor(Qt.PointingHandCursor)
        self.square_box.setCursor(Qt.PointingHandCursor)
        self.center_box.setCursor(Qt.PointingHandCursor)

        self.apply_new_color(self.my_color)

        self.button_new_file.clicked.connect(self.select_new_file)

        self.box_isdynamic.stateChanged.connect(self.new_state)
        self.scroll_step.valueChanged.connect(self.step_changed)
        self.scroll_color.valueChanged.connect(self.new_range_color)
        self.buttonLoad.clicked.connect(self.calltracker)
        self.scroll_combine.valueChanged.connect(self.combines_shapes_box)

        self.containImage.messager.pixel_selected.connect(self.apply_newpixel_selected)
        self.containImage.messager.transfert_position.connect(self.display_temporary_color)
        self.containImage.messager.selecter_leaved.connect(self.apply_selecter_leaved)

        self.point_box.stateChanged.connect(self.show_hide_points)
        self.square_box.stateChanged.connect(self.show_hide_rects)
        self.center_box.stateChanged.connect(self.show_hide_middle)

    @Slot()
    def calltracker(self):
        count = time.time()
        self.shapes = start_tracker(self.map, self.size, self.step, self.min_color, self.max_color, self.compiler_value)
        self.display_calctime.setText(str(round(time.time() - count, 5)))

        count = time.time()
        self.build_graph()
        self.display_graph_sec.setText(str(round(time.time() - count, 5)))

        self.display_nbr_item.setText(str(len(self.shapes)))

    @Slot(int)
    def step_changed(self, value):
        self.value_step.setText(str(value))
        self.step = value

        if self.compiler_value == 0:
            self.display_combine_range.setText("Off")
        else:
            self.display_combine_range.setText(str(self.step * self.compiler_value))

        if self.are_dynamic_settings:
            self.calltracker()

    @Slot(int)
    def combines_shapes_box(self, value):
        self.compiler_value = value

        if self.compiler_value == 0:
            self.display_combine_range.setText("Off")
        else:
            self.display_combine_range.setText(str(self.step * self.compiler_value))

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
        pix_color = QPixmap(100, 100)
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
    def display_temporary_color(self, x, y):
        color_in_pixmap = QPixmap(100, 100)
        pixel = self.map[x, y]

        color_in_pixmap.fill(QColor(pixel[0], pixel[1], pixel[2]))
        self.dynamic_color_label.setPixmap(color_in_pixmap)

    @Slot(int, int)
    def apply_newpixel_selected(self, x, y):
        self.apply_new_color(self.map[x, y])
        if self.are_dynamic_settings:
            self.calltracker()

    @Slot()
    def apply_selecter_leaved(self):
        color_pix = QPixmap(50, 50)
        color_pix.fill(Qt.transparent)
        self.dynamic_color_label.setPixmap(color_pix)

    @Slot(int)
    def show_hide_points(self, value):
        if value == 2:
            self.point_visibles = True
        else:
            self.point_visibles = False
        self.build_graph()

    @Slot(int)
    def show_hide_rects(self, value):
        if value == 2:
            self.rect_visibles = True
        else:
            self.rect_visibles = False
        self.build_graph()

    @Slot(int)
    def show_hide_middle(self, value):
        if value == 2:
            self.middle_visible = True
        else:
            self.middle_visible = False
        self.build_graph()

    def build_graph(self):
        self.scene.setSceneRect(0, 0, self.size[0], self.size[1])
        self.scene.clear()

        color_point = QPen(Qt.white)
        point_with = 2
        color_square = QPen("#ff0048")
        color_square.setWidth(2)
        color_middle = QPen("#0084ff")
        color_middle.setWidth(2)
        middle_width = 10

        self.scene.addPixmap(self.low_pixmap)

        for i in range(len(self.shapes)):
            if self.point_visibles:
                for j in range(len(self.shapes[i].point_cloud)):
                    self.scene.addLine(self.shapes[i].point_cloud[j][0] - point_with, self.shapes[i].point_cloud[j][1], self.shapes[i].point_cloud[j][0] + point_with, self.shapes[i].point_cloud[j][1], color_point)
                    self.scene.addLine(self.shapes[i].point_cloud[j][0], self.shapes[i].point_cloud[j][1] - point_with, self.shapes[i].point_cloud[j][0], self.shapes[i].point_cloud[j][1] + point_with, color_point)
            if self.rect_visibles:
                self.scene.addRect(QRect(self.shapes[i].top_left[0], self.shapes[i].top_left[1], self.shapes[i].width, self.shapes[i].height), color_square)
            if self.middle_visible:
                self.scene.addLine(self.shapes[i].center[0] - middle_width, self.shapes[i].center[1], self.shapes[i].center[0] + middle_width, self.shapes[i].center[1], color_middle)
                self.scene.addLine(self.shapes[i].center[0], self.shapes[i].center[1] - middle_width, self.shapes[i].center[0], self.shapes[i].center[1] + middle_width, color_middle)

        self.graphic_view.setScene(self.scene)

    def load_image(self):
        image = QImage(self.image_url)
        painter = QPainter()

        painter.begin(image)
        painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        painter.fillRect(image.rect(), QColor(0, 0, 0, 50))
        painter.end()

        self.scene.clear()
        self.low_pixmap = QPixmap(image)
        self.scene.addPixmap(self.low_pixmap)
        self.graphic_view.setScene(self.scene)

        self.containImage.setPixmap(QPixmap(self.image_url))
        self.my_image = Image.open(self.image_url)
        self.map = self.my_image.load()
        self.size = self.my_image.size

        self.containImage.setFixedSize(self.size[0], self.size[1])
        self.graphic_view.setFixedSize(self.size[0], self.size[1])

        if self.size[0] > self.size[1]:
            self.mainGridLayout.addWidget(self.graphic_view, 1, 0)
            self.mainGridLayout.addWidget(self.settingswidget, 0, 1, 2, 1)
        else:
            self.mainGridLayout.addWidget(self.graphic_view, 0, 1)
            self.mainGridLayout.addWidget(self.settingswidget, 0, 2, 2, 1)

    def select_new_file(self):
        container = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg)")
        if not container[0] == "":
            self.image_url = container[0]
            self.load_image()

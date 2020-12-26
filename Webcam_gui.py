from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from numpy import *
from PIL import Image
import cv2
import sys
from ViewPicker import *
from Cam_tracker import *
from Dynamic_shape import *

class Thread(QThread):
    change_pixmap = Signal(QImage)
    change_map = Signal(list)
    camera_size = Signal(list)

    def run(self):
        my_width = 1920
        my_height = 1080
        cap = cv2.VideoCapture(0)
        fps = cap.get(cv2.CAP_PROP_FPS)  # Print fps

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, my_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, my_height)

        cap.set(10, 4)  # SET BRIGHNESS TO 5
        cap.set(12, 20)  # SET SATURATION TO 10

        self.camera_size.emit([cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)])
        print("SIZE: " + str(my_width) + ", " + str(my_height))
        print("FPS: " + str(fps))

        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                self.change_pixmap.emit(convertToQtFormat)
                self.change_map.emit(rgbImage)

class Webcam_gui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.my_thread = 0
        self.player_color = 0
        self.hover_rgb = 0
        self.min_rgb = (0, 0, 0)
        self.mid_rgb = (0, 0, 0)
        self.max_rgb = (0, 0, 0)
        self.color_range = 30
        self.run_tracking = False
        self.shape = Dynamic_shape()
        self.current_map = []
        self.timer_count = 0
        self.camera_size = [0, 0]

        self.main_layout = QGridLayout(self)
        self.graphic_scene = QGraphicsScene(self)
        self.graphic_view_picker = ViewPicker()

        self.color_box = QGroupBox("Color", self)
        self.color_layout = QGridLayout(self)
        self.text_color = QLabel("Hovered", self)
        self.hover_color = QLabel(self)
        self.min_color = QLabel(self)
        self.mid_color = QLabel(self)
        self.top_color = QLabel(self)
        self.color_slider = QSlider(self)
        self.color_value_label = QLabel(str(self.color_range), self)

        self.group_item = QGroupBox("Navigation", self)
        self.item_layout = QGridLayout(self)
        self.position_text = QLabel("Position", self)
        self.x_indicator = QLabel("X", self)
        self.x_value = QLabel("0", self)
        self.y_indicator = QLabel("Y", self)
        self.y_value = QLabel("0", self)
        self.diameter_text = QLabel("Diameter", self)
        self.diameter_value = QLabel("0 pixels", self)
        self.screen_text = QLabel("Side", self)
        self.arrow_layout = QGridLayout(self)
        self.arrow_top = QLabel(self)
        self.arrow_right = QLabel(self)
        self.arrow_bot = QLabel(self)
        self.arrow_left = QLabel(self)
        self.top_side = [0, 0]
        self.right_side = [0, 0]
        self.bot_side = [0, 0]
        self.left_side = [0, 0]

        self.top_pixmap_off = QPixmap("images/top_arrow_off.png")
        self.right_pixmap_off = QPixmap("images/right_arrow_off.png")
        self.bot_pixmap_off = QPixmap("images/bot_arrow_off.png")
        self.left_pixmap_off = QPixmap("images/left_arrow_off.png")
        self.top_pixmap_on = QPixmap("images/top_arrow.png")
        self.right_pixmap_on = QPixmap("images/right_arrow.png")
        self.bot_pixmap_on = QPixmap("images/bot_arrow.png")
        self.left_pixmap_on = QPixmap("images/left_arrow.png")

        self.box_time = QGroupBox("Time", self)
        self.time_layout = QVBoxLayout(self)
        self.calc_time = QLabel("Calc time", self)
        self.timer_display = QLabel("0", self)
        self.text_possible_iterations = QLabel("Possible iterations", self)
        self.iterations_sec = QLabel("0", self)

        self.button_tracking = QPushButton("Tracking Off", self)

        self.set_up_camera()
        self.build_ui()

    def build_ui(self):
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.graphic_view_picker, 0, 0, 4, 1)

        self.main_layout.addWidget(self.color_box, 0, 1)
        self.color_box.setLayout(self.color_layout)

        self.color_layout.addWidget(self.text_color, 0, 0, 1, 2)
        self.color_layout.addWidget(self.hover_color, 0, 2)
        self.color_layout.addWidget(self.min_color, 1, 0)
        self.color_layout.addWidget(self.mid_color, 1, 1)
        self.color_layout.addWidget(self.top_color, 1, 2)
        self.color_layout.addWidget(self.color_slider, 2, 0, 1, 2)
        self.color_layout.addWidget(self.color_value_label, 2, 2)

        self.main_layout.addWidget(self.group_item, 1, 1)
        self.group_item.setLayout(self.item_layout)
        self.item_layout.addWidget(self.position_text, 0, 0, 1, 4)
        self.item_layout.addWidget(self.x_indicator, 1, 0)
        self.item_layout.addWidget(self.x_value, 1, 1)
        self.item_layout.addWidget(self.y_indicator, 1, 2)
        self.item_layout.addWidget(self.y_value, 1, 3)
        self.item_layout.addWidget(self.diameter_text, 2, 0, 1, 4)
        self.item_layout.addWidget(self.diameter_value, 3, 0, 1, 4)
        self.item_layout.addWidget(self.screen_text, 4, 0, 1, 2)

        self.item_layout.addLayout(self.arrow_layout, 4, 2, 1, 2, Qt.AlignRight)
        self.arrow_layout.addWidget(self.arrow_top, 0, 1)
        self.arrow_layout.addWidget(self.arrow_right, 1, 2)
        self.arrow_layout.addWidget(self.arrow_bot, 2, 1)
        self.arrow_layout.addWidget(self.arrow_left, 1, 0)

        self.main_layout.addWidget(self.box_time, 2, 1)
        self.box_time.setLayout(self.time_layout)
        self.time_layout.addWidget(self.calc_time)
        self.time_layout.addWidget(self.timer_display)
        self.time_layout.addWidget(self.text_possible_iterations)
        self.time_layout.addWidget(self.iterations_sec)

        self.main_layout.addWidget(self.button_tracking, 3, 1)

        self.hover_color.setFixedSize(80, 40)
        self.min_color.setFixedSize(80, 40)
        self.mid_color.setFixedSize(80, 40)
        self.top_color.setFixedSize(80, 40)

        self.graphic_view_picker.setScene(self.graphic_scene)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.color_layout.setAlignment(Qt.AlignTop)

        self.color_slider.setOrientation(Qt.Horizontal)
        self.color_slider.setRange(0, 50)
        self.color_slider.setValue(30)
        self.color_slider.setPageStep(1)
        self.color_slider.setCursor(Qt.PointingHandCursor)

        self.item_layout.setAlignment(Qt.AlignTop)
        self.arrow_layout.setContentsMargins(0, 0, 0, 0)
        self.top_pixmap_off = self.top_pixmap_off.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.right_pixmap_off = self.right_pixmap_off.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.bot_pixmap_off = self.bot_pixmap_off.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.left_pixmap_off = self.left_pixmap_off.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.top_pixmap_on = self.top_pixmap_on.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.right_pixmap_on = self.right_pixmap_on.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.bot_pixmap_on = self.bot_pixmap_on.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.left_pixmap_on = self.left_pixmap_on.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.arrow_top.setPixmap(self.top_pixmap_off)
        self.arrow_right.setPixmap(self.right_pixmap_off)
        self.arrow_bot.setPixmap(self.bot_pixmap_off)
        self.arrow_left.setPixmap(self.left_pixmap_off)

        self.color_slider.valueChanged.connect(self.apply_color_range)
        self.graphic_view_picker.messager.transfert_position.connect(self.hover_position)
        self.graphic_view_picker.messager.pixel_selected.connect(self.new_color_clicked)
        self.graphic_view_picker.messager.pixel_selected.connect(self.new_color_clicked)
        self.button_tracking.clicked.connect(self.button_track_clicked)

    def set_up_camera(self):
        self.my_thread = Thread(self)
        self.my_thread.camera_size.connect(self.set_up_camera_size)
        self.my_thread.change_pixmap.connect(self.setImage)
        self.my_thread.change_map.connect(self.set_map)
        self.my_thread.start()

    @Slot(QImage)
    def setImage(self, image):
        self.graphic_scene.clear()

        self.graphic_scene.addPixmap(QPixmap.fromImage(image))


    @Slot(list)
    def set_map(self, map):
        self.current_map = map

        if self.run_tracking:
            count = time.time()
            data_shape = cam_tracker(self.current_map)
            self.shape.build(data_shape[0], data_shape[1], data_shape[2], data_shape[3])
            self.draw_shape()
            self.apply_new_color(data_shape[4])
            self.paint_arrow()

            self.timer_count += 1
            if self.timer_count > 5:
                self.update_item_box()
                self.timer_display.setText(str(round(time.time() - count, 5)))
                self.iterations_sec.setText(str(round(1/(time.time() - count))))
                self.timer_count = 0

    @Slot(int, int)
    def hover_position(self, x, y):
        self.hover_rgb = self.current_map[y][x]

        pix_color = QPixmap(100, 100)
        pix_color.fill(QColor(self.hover_rgb[0], self.hover_rgb[1], self.hover_rgb[2]))
        self.hover_color.setPixmap(pix_color)

    @Slot(int, int)
    def new_color_clicked(self, x, y):
        self.apply_new_color(self.current_map[y][x])

        new_pos(x, y, self.mid_rgb, self.color_range, len(self.current_map[0]), len(self.current_map))
        self.run_tracking = True
        self.button_tracking.setText("Tracking On")

    def apply_new_color(self, newcolor):
        pix_color = QPixmap(100, 100)
        pix_color.fill(QColor(newcolor[0], newcolor[1], newcolor[2]))

        self.mid_rgb = newcolor
        self.mid_color.setPixmap(pix_color)

        # Set Min Color
        rgb_color = [self.mid_rgb[0], self.mid_rgb[1], self.mid_rgb[2]]
        for i in range(len(rgb_color)):
            rgb_color[i] -= self.color_range
            if rgb_color[i] < 0:
                rgb_color[i] = 0

        self.min_rgb = (rgb_color[0], rgb_color[1], rgb_color[2])
        pix_color.fill(QColor(self.min_rgb[0], self.min_rgb[1], self.min_rgb[2]))
        self.min_color.setPixmap(pix_color)

        # Set Max Color
        rgb_color = [self.mid_rgb[0], self.mid_rgb[1], self.mid_rgb[2]]
        for i in range(len(rgb_color)):
            rgb_color[i] += self.color_range
            if 255 < rgb_color[i]:
                rgb_color[i] = 255

        self.max_rgb = (rgb_color[0], rgb_color[1], rgb_color[2])
        pix_color.fill(QColor(self.max_rgb[0], self.max_rgb[1], self.max_rgb[2]))
        self.top_color.setPixmap(pix_color)

    def draw_shape(self):
        color_square = QPen("#ff0048")
        color_square.setWidth(2)
        color_middle = QPen("#0084ff")
        color_middle.setWidth(2)
        middle_width = 10

        self.graphic_scene.addRect(QRect(self.shape.top_left[0], self.shape.top_left[1], self.shape.width, self.shape.height), color_square)

        self.graphic_scene.addLine(self.shape.center[0] - middle_width, self.shape.center[1], self.shape.center[0] + middle_width, self.shape.center[1], color_middle)
        self.graphic_scene.addLine(self.shape.center[0], self.shape.center[1] - middle_width, self.shape.center[0], self.shape.center[1] + middle_width, color_middle)


    def __del__(self):
        del self.my_thread


    @Slot(int)
    def apply_color_range(self, value):
        self.color_range = value
        self.color_value_label.setText(str(value))
        new_color_range(value)

    def update_item_box(self):
        self.x_value.setText(str(int(self.shape.center[0])))
        self.y_value.setText(str(int(self.shape.center[1])))

        if self.shape.width > self.shape.height:
            self.diameter_value.setText(str(self.shape.height) + " pixels")
        else:
            self.diameter_value.setText(str(self.shape.width) + " pixels")


    @Slot(list)
    def set_up_camera_size(self, size):
        self.camera_size = size
        print(str(size))
        self.graphic_view_picker.setFixedSize(size[0], size[1])

        self.top_side = [0, int((size[1]/5) * 2)]
        self.right_side = [int((size[0]/5) * 3), int(size[0])]
        self.bot_side = [int((size[1]/5) * 3), int(size[1])]
        self.left_side = [0, int((size[0] / 5) * 2)]


    @Slot()
    def button_track_clicked(self):
        if self.run_tracking:
            self.run_tracking = False
            self.button_tracking.setText("Tracking Off")
        else:
            self.run_tracking = True
            self.button_tracking.setText("Tracking On")


    def paint_arrow(self):
        if self.left_side[0] <= self.shape.center[0] <= self.left_side[1]:
            self.arrow_left.setPixmap(self.left_pixmap_on)
            self.arrow_right.setPixmap(self.right_pixmap_off)
        elif self.right_side[0] <= self.shape.center[0] <= self.right_side[1]:
            self.arrow_left.setPixmap(self.left_pixmap_off)
            self.arrow_right.setPixmap(self.right_pixmap_on)
        else:
            self.arrow_left.setPixmap(self.left_pixmap_off)
            self.arrow_right.setPixmap(self.right_pixmap_off)

        if self.top_side[0] <= self.shape.center[1] <= self.top_side[1]:
            self.arrow_top.setPixmap(self.top_pixmap_on)
            self.arrow_bot.setPixmap(self.bot_pixmap_off)
        elif self.bot_side[0] <= self.shape.center[1] <= self.bot_side[1]:
            self.arrow_top.setPixmap(self.top_pixmap_off)
            self.arrow_bot.setPixmap(self.bot_pixmap_on)
        else:
            self.arrow_bot.setPixmap(self.bot_pixmap_off)
            self.arrow_top.setPixmap(self.top_pixmap_off)





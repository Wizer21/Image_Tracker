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
import json

class Thread(QThread):
    change_pixmap = Signal(QImage)
    change_map = Signal(list)
    camera_param = Signal(list)

    def run(self):
        my_width = 1920
        my_height = 1080
        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, my_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, my_height)
        cap.set(10, 4)  # SET BRIGHNESS TO 5
        cap.set(12, 20)  # SET SATURATION TO 10

        self.camera_param.emit([cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(cv2.CAP_PROP_FPS)])

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
        self.my_thread = Thread(self)
        self.player_color = 0
        self.hover_rgb = 0
        self.min_rgb = (0, 0, 0)
        self.mid_rgb = (0, 0, 0)
        self.max_rgb = (0, 0, 0)
        self.color_range = 15
        self.run_tracking = False
        self.shape = Dynamic_shape()
        self.current_map = []
        self.timer_count = 0
        self.camera_size = [0, 0]
        self.show_points = False
        self.show_center = True
        self.show_rect = True
        self.pen_size = 5
        self.slow_motion = False
        self.calibration_on = False
        self.building_preset = False
        self.calibration_stack = 0
        self.calibration_count = 0
        self.new_preset = {}
        self.presets_list = {}
        self.current_preset = {}
        self.is_width_entered = False
        self.getting_width = False
        self.item_width = 0

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
        self.resolution_display = QLabel("Resolution", self)
        self.resolution = QLabel("0", self)
        self.fps_display = QLabel("FPS", self)
        self.fps = QLabel("0", self)
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

        self.draw_box = QGroupBox("Draw", self)
        self.draw_layout = QGridLayout()
        self.point_text = QLabel("Show points", self)
        self.check_points = QCheckBox()
        self.squares_text = QLabel("Show squares", self)
        self.check_squares = QCheckBox()
        self.center_text = QLabel("Show center", self)
        self.check_center = QCheckBox()
        self.draw_size = QLabel("Draw width", self)
        self.draw_size_slider = QSlider()
        self.draw_size_display_value = QLabel(str(self.pen_size), self)
        self.slow_motion_text = QLabel("Slow motion", self)
        self.slow_box = QCheckBox(self)

        self.distance_box = QGroupBox("Distance", self)  # DISTANCE
        self.distance_layout = QGridLayout(self)

        self.calibrate_box = QGroupBox("Calibrate", self)
        self.calibrate_layout = QGridLayout(self)
        self.presets_text = QLabel("Presets", self)
        self.combo_presets = QComboBox(self)
        self.ratio_current_preset = QLabel("No presets", self)
        self.name_edit = QLineEdit(self)
        self.width_edit_calib = QLineEdit(self)
        self.distance_edit_calib = QLineEdit(self)
        self.save_button = QPushButton("Save preset", self)

        self.text_shape_diameter = QLabel("My Item Diameter", self)
        self.text_distance = QLabel("From Distance", self)
        self.distance_edit = QLineEdit(self)
        self.diameter_calcul_button = QPushButton("Calculate", self)
        self.diameter_edit = QLineEdit(self)
        self.text_result_distance = QLabel("Distance", self)
        self.distance_result = QLabel("0", self)

        self.set_up_camera()
        self.build_ui()

    def build_ui(self):
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.graphic_view_picker, 0, 0, 5, 1)

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
        self.item_layout.addWidget(self.resolution_display, 0, 0, 1, 4)
        self.item_layout.addWidget(self.resolution, 1, 0, 1, 4)
        self.item_layout.addWidget(self.fps_display, 2, 0, 1, 4)
        self.item_layout.addWidget(self.fps, 3, 0, 1, 4)
        self.item_layout.addWidget(self.position_text, 4, 0, 1, 4)
        self.item_layout.addWidget(self.x_indicator, 5, 0)
        self.item_layout.addWidget(self.x_value, 5, 1)
        self.item_layout.addWidget(self.y_indicator, 5, 2)
        self.item_layout.addWidget(self.y_value, 5, 3)
        self.item_layout.addWidget(self.diameter_text, 6, 0, 1, 4)
        self.item_layout.addWidget(self.diameter_value, 7, 0, 1, 4)
        self.item_layout.addWidget(self.screen_text, 8, 0, 1, 2)

        self.item_layout.addLayout(self.arrow_layout, 8, 2, 1, 2, Qt.AlignRight)
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

        self.main_layout.addWidget(self.draw_box, 4, 1)
        self.draw_box.setLayout(self.draw_layout)
        self.draw_layout.addWidget(self.check_points, 0, 0)
        self.draw_layout.addWidget(self.point_text, 0, 1, 1, 2)
        self.draw_layout.addWidget(self.check_squares, 1, 0)
        self.draw_layout.addWidget(self.squares_text, 1, 1, 1, 2)
        self.draw_layout.addWidget(self.check_center, 2, 0)
        self.draw_layout.addWidget(self.center_text, 2, 1, 1, 2)
        self.draw_layout.addWidget(self.draw_size, 3, 0, 1, 3)
        self.draw_layout.addWidget(self.draw_size_slider, 4, 0, 1, 2)
        self.draw_layout.addWidget(self.draw_size_display_value, 4, 2)
        self.draw_layout.addWidget(self.slow_box, 5, 0)
        self.draw_layout.addWidget(self.slow_motion_text, 5, 1, 1, 2)
        self.draw_layout.setColumnStretch(0, 0)
        self.draw_layout.setColumnStretch(1, 1)

        self.main_layout.addWidget(self.distance_box, 0, 2, 2, 1)  # DISTANCE
        self.distance_box.setLayout(self.distance_layout)
        self.distance_layout.addWidget(self.calibrate_box, 0, 0, 1, 2)

        self.calibrate_box.setLayout(self.calibrate_layout)
        self.calibrate_layout.addWidget(self.presets_text, 0, 0)
        self.calibrate_layout.addWidget(self.combo_presets, 0, 1)
        self.calibrate_layout.addWidget(self.ratio_current_preset, 1, 0, 1, 2)
        self.calibrate_layout.addWidget(self.name_edit, 2, 0, 1, 2)
        self.calibrate_layout.addWidget(self.width_edit_calib, 3, 0)
        self.calibrate_layout.addWidget(self.distance_edit_calib, 3, 1)
        self.calibrate_layout.addWidget(self.save_button, 4, 0, 1, 2)

        self.distance_layout.addWidget(self.text_shape_diameter, 1, 0, 1, 2)
        self.distance_layout.addWidget(self.text_distance, 2, 0)
        self.distance_layout.addWidget(self.distance_edit, 2, 1)
        self.distance_layout.addWidget(self.diameter_calcul_button, 3, 0, 1, 2)
        self.distance_layout.addWidget(self.diameter_edit, 4, 0, 1, 2)
        self.distance_layout.addWidget(self.text_result_distance, 5, 0, 1, 2)
        self.distance_layout.addWidget(self.distance_result, 6, 0, 1, 2)

        self.hover_color.setFixedSize(80, 40)
        self.min_color.setFixedSize(80, 40)
        self.mid_color.setFixedSize(80, 40)
        self.top_color.setFixedSize(80, 40)

        self.graphic_view_picker.setScene(self.graphic_scene)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.color_layout.setAlignment(Qt.AlignTop)

        self.color_slider.setOrientation(Qt.Horizontal)
        self.color_slider.setRange(0, 50)
        self.color_slider.setValue(self.color_range)
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

        self.time_layout.setAlignment(Qt.AlignTop)

        self.arrow_top.setPixmap(self.top_pixmap_off)
        self.arrow_right.setPixmap(self.right_pixmap_off)
        self.arrow_bot.setPixmap(self.bot_pixmap_off)
        self.arrow_left.setPixmap(self.left_pixmap_off)

        self.button_tracking.setCursor(Qt.PointingHandCursor)

        self.draw_size_slider.setOrientation(Qt.Horizontal)
        self.draw_size_slider.setRange(1, 20)
        self.draw_size_slider.setValue(self.pen_size)
        self.draw_size_slider.setPageStep(1)
        self.draw_size_slider.setCursor(Qt.PointingHandCursor)
        self.check_squares.setChecked(True)
        self.check_center.setChecked(True)
        self.check_points.setCursor(Qt.PointingHandCursor)
        self.check_squares.setCursor(Qt.PointingHandCursor)
        self.check_center.setCursor(Qt.PointingHandCursor)
        self.slow_box.setCursor(Qt.PointingHandCursor)

        self.distance_layout.setAlignment(Qt.AlignTop)  # DISTANCE

        self.name_edit.setPlaceholderText("Preset 1")
        self.width_edit_calib.setPlaceholderText("Width cm")
        self.distance_edit_calib.setPlaceholderText("Dist. cm")
        self.distance_edit.setPlaceholderText("Dist. cm")
        self.diameter_edit.setPlaceholderText("Item, min diameter possible")

        self.width_edit_calib.setToolTip("Item width in cm")
        self.distance_edit_calib.setToolTip("Distance from the camera in cm")
        self.distance_edit.setToolTip("Distance from the camera in cm")
        self.diameter_edit.setToolTip("Item width in cm")

        self.combo_presets.setCursor(Qt.PointingHandCursor)
        self.name_edit.setCursor(Qt.PointingHandCursor)
        self.width_edit_calib.setCursor(Qt.PointingHandCursor)
        self.distance_edit_calib.setCursor(Qt.PointingHandCursor)
        self.distance_edit.setCursor(Qt.PointingHandCursor)
        self.diameter_edit.setCursor(Qt.PointingHandCursor)
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.diameter_calcul_button.setCursor(Qt.PointingHandCursor)

        try:
            with open("presets.json", "r") as dataFile:
                self.presets_list = json.load(dataFile)
        except FileNotFoundError:
            with open("presets.json", "w") as dataFile:
                self.presets_list["Default"] = {
                    "name": "Default",
                    "width": 1,
                    "distance": 10,
                    "pixel": 20
                }
                json.dump(self.presets_list, dataFile)
            print("Presets file created")

        for i in self.presets_list:
            self.combo_presets.addItem(i)

        self.set_current_preset(self.combo_presets.currentText())

        self.color_slider.valueChanged.connect(self.apply_color_range)  # CONNECTIONS
        self.graphic_view_picker.messager.transfert_position.connect(self.hover_position)
        self.graphic_view_picker.messager.pixel_selected.connect(self.new_color_clicked)
        self.graphic_view_picker.messager.pixel_selected.connect(self.new_color_clicked)
        self.graphic_view_picker.messager.selecter_leaved.connect(self.picker_leaved)
        self.button_tracking.clicked.connect(self.button_track_clicked)

        self.draw_size_slider.valueChanged.connect(self.apply_draw_value)
        self.check_points.stateChanged.connect(self.apply_show_points)
        self.check_squares.stateChanged.connect(self.apply_show_squares)
        self.check_center.stateChanged.connect(self.apply_show_centers)
        self.slow_box.stateChanged.connect(self.apply_is_slow_motion)

        self.save_button.clicked.connect(self.new_preset_clicked)
        self.combo_presets.textActivated.connect(self.set_current_preset)
        self.diameter_calcul_button.clicked.connect(self.set_diameter_from_range)
        self.diameter_edit.textChanged.connect(self.set_new_item_width)


    def set_up_camera(self):
        self.my_thread.camera_param.connect(self.set_up_camera_param)
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

            if self.slow_motion:
                if self.timer_count > 5:
                    self.shape.build(data_shape[0], data_shape[1], data_shape[2], data_shape[3], data_shape[4])
            else:
                self.shape.build(data_shape[0], data_shape[1], data_shape[2], data_shape[3], data_shape[4])

            self.draw_shape()
            self.apply_new_color(data_shape[5])
            self.paint_arrow()

            if self.timer_count > 6:
                self.update_item_box()
                self.timer_display.setText(str(round(time.time() - count, 5)))
                self.iterations_sec.setText(str(round(1/(time.time() - count))))
                self.timer_count = 0
            self.timer_count += 1

            if self.calibration_on:
                self.calibration_count += 1
                self.calibration_stack += data_shape[6]
                if self.calibration_count > 100:
                    self.calibration_on = False
                    self.new_preset["pixel"] = (round(self.calibration_stack / self.calibration_count, 3))
                    if self.building_preset:
                        self.building_preset = False
                        self.build_preset()
                    elif self.getting_width:
                        self.getting_width = False
                        self.diameter_from_range()


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


    @Slot()
    def picker_leaved(self):
        self.hover_color.clear()


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
        color_points = QPen("#ffffff")
        color_points.setWidth(self.pen_size)
        color_square = QPen("#ff0048")
        color_square.setWidth(self.pen_size)
        color_middle = QPen("#0084ff")
        color_middle.setWidth(self.pen_size)
        middle_width = 10

        if self.show_points:
            points = self.shape.points
            for i in range(len(self.shape.points)):
                self.graphic_scene.addLine(points[i][0] - self.pen_size, points[i][1], points[i][0] + self.pen_size, points[i][1], color_points)
                self.graphic_scene.addLine(points[i][0], points[i][1] - self.pen_size, points[i][0], points[i][1] + self.pen_size, color_points)
        if self.show_rect:
            self.graphic_scene.addRect(QRect(self.shape.top_left[0], self.shape.top_left[1], self.shape.width, self.shape.height), color_square)
        if self.show_center:
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
    def set_up_camera_param(self, data):
        self.camera_size = data
        self.graphic_view_picker.setFixedSize(data[0], data[1])

        self.top_side = [0, int((data[1]/5) * 2)]
        self.right_side = [int((data[0]/5) * 3), int(data[0])]
        self.bot_side = [int((data[1]/5) * 3), int(data[1])]
        self.left_side = [0, int((data[0] / 5) * 2)]

        self.resolution.setText(str(int(data[0])) + " x " + str(int(data[1])))
        self.fps.setText(str(int(data[2])))


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


    @Slot(int)
    def apply_draw_value(self, value):
        self.pen_size = value
        self.draw_size_display_value.setText(str(value))


    @Slot(int)
    def apply_show_points(self, value):
        if value == 2:
            self.show_points = True
        else:
            self.show_points = False


    @Slot(int)
    def apply_show_squares(self, value):
        if value == 2:
            self.show_rect = True
        else:
            self.show_rect = False


    @Slot(int)
    def apply_show_centers(self, value):
        if value == 2:
            self.show_center = True
        else:
            self.show_center = False


    @Slot(int)
    def apply_is_slow_motion(self, value):
        if value == 2:
            self.slow_motion = True
        else:
            self.slow_motion = False


    @Slot()
    def new_preset_clicked(self):
        if len(self.name_edit.text()) == 0 or \
        len(self.width_edit_calib.text()) == 0 or \
        len(self.distance_edit_calib.text()) == 0:
            print("Empty data")
            return
        if not self.run_tracking:
            print("Tracking Off")
            return
        if self.name_edit.text() in self.presets_list:
            print("Existing preset")
            return

        self.new_preset.clear()
        self.new_preset["name"] = (self.name_edit.text())
        self.new_preset["width"] = float((self.width_edit_calib.text()))
        self.new_preset["distance"] = float((self.distance_edit_calib.text()))

        self.calibration_stack = 0
        self.calibration_count = 0
        self.building_preset = True
        self.calibration_on = True


    def build_preset(self):
        self.new_preset["pixel"] = round(self.new_preset["pixel"] * (1/self.new_preset["width"]), 3)
        self.new_preset["width"] = 1

        self.combo_presets.addItem(self.new_preset["name"])
        self.presets_list[self.new_preset["name"]] = self.new_preset

        with open("presets.json", "w") as dataFile:
            json.dump(self.presets_list, dataFile)

        self.set_current_preset(self.new_preset["name"])


    @Slot(str)
    def set_current_preset(self, preset_name):
        self.current_preset = self.presets_list[preset_name]

        preset = self.presets_list[preset_name]
        self.ratio_current_preset.setText(str(preset["width"]) + "cm at " + str(round(preset["distance"], 2)) + "cm = " + str(preset["pixel"]) + "px")


    @Slot(str)
    def set_diameter_from_range(self, value):
        self.calibration_stack = 0
        self.calibration_count = 0
        self.getting_width = True
        self.calibration_on = True


    def diameter_from_range(self):
        item_width = round(1/(self.current_preset["pixel"]/(self.calibration_stack / self.calibration_count)), 3)
        self.diameter_edit.setText(str(item_width))


    def set_new_item_width(self):
        self.item_width = float(self.diameter_edit.text())
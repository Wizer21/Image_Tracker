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
    changePixmap = Signal(QImage)
    video_size = Signal(int, int)


    def run(self):
        my_widht = 1920
        my_height = 1080
        cap = cv2.VideoCapture(0)
        fps = cap.get(cv2.CAP_PROP_FPS)  # Print fps

        # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  #Permit to get native size
        # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        cap.set(10, 4)  # SET BRIGHNESS TO 5
        cap.set(12, 20)  # SET SATURATION TO 10

        self.video_size.emit(my_widht, my_height)
        print("SIZE: " + str(my_widht) + ", " + str(my_height))
        print("FPS: " + str(fps))

        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                image_qt = convertToQtFormat.scaled(my_widht, my_height, Qt.KeepAspectRatio)
                self.changePixmap.emit(image_qt)

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
        self.cam_current_image = QImage()
        self.timer_count = 0

        self.main_layout = QGridLayout(self)
        self.graphic_scene = QGraphicsScene(self)
        self.graphic_view_picker = ViewPicker()

        self.color_box = QGroupBox(self)
        self.color_layout = QGridLayout(self)
        self.text_color = QLabel(self)
        self.hover_color = QLabel(self)
        self.min_color = QLabel(self)
        self.mid_color = QLabel(self)
        self.top_color = QLabel(self)
        self.color_slider = QSlider(self)
        self.color_value_label = QLabel(self)

        self.text_possible_iterations = QLabel(self)
        self.iterations_sec = QLabel(self)

        self.set_up_camera()
        self.build_ui()

    def build_ui(self):
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.graphic_view_picker, 0, 0)
        self.main_layout.addWidget(self.color_box, 0, 1)
        self.color_box.setLayout(self.color_layout)

        self.color_layout.addWidget(self.text_color, 0, 0, 1, 2)
        self.color_layout.addWidget(self.hover_color, 0, 2)
        self.color_layout.addWidget(self.min_color, 1, 0)
        self.color_layout.addWidget(self.mid_color, 1, 1)
        self.color_layout.addWidget(self.top_color, 1, 2)
        self.color_layout.addWidget(self.color_slider, 2, 0, 1, 2)
        self.color_layout.addWidget(self.color_value_label, 2, 2)

        self.main_layout.addWidget(self.text_possible_iterations, 1, 1)
        self.main_layout.addWidget(self.iterations_sec, 2, 1)

        self.hover_color.setFixedSize(80, 40)
        self.min_color.setFixedSize(80, 40)
        self.mid_color.setFixedSize(80, 40)
        self.top_color.setFixedSize(80, 40)

        self.graphic_view_picker.setScene(self.graphic_scene)
        self.main_layout.setAlignment(Qt.AlignTop and Qt.AlignRight)
        self.color_layout.setAlignment(Qt.AlignTop)
        self.color_box.setTitle("Color")
        self.text_color.setText("Hovered")
        self.color_value_label.setText(str(self.color_range))

        self.color_slider.setOrientation(Qt.Horizontal)
        self.color_slider.setRange(0, 50)
        self.color_slider.setValue(30)
        self.color_slider.setPageStep(1)
        self.color_slider.setCursor(Qt.PointingHandCursor)

        self.text_possible_iterations.setText("Possible iterations")
        self.iterations_sec.setText("0")

        self.color_slider.valueChanged.connect(self.apply_color_range)
        self.graphic_view_picker.messager.transfert_position.connect(self.hover_position)
        self.graphic_view_picker.messager.pixel_selected.connect(self.new_color_clicked)
        self.graphic_view_picker.messager.pixel_selected.connect(self.new_color_clicked)


    def set_up_camera(self):
        self.my_thread = Thread(self)
        self.my_thread.changePixmap.connect(self.setImage)
        self.my_thread.video_size.connect(self.apply_camera_size)
        self.my_thread.start()

    @Slot(QImage)
    def setImage(self, image):
        self.graphic_scene.clear()
        count = time.time()

        self.graphic_scene.addPixmap(QPixmap.fromImage(image))
        self.cam_current_image = image

        if self.run_tracking:
            data_shape = cam_tracker(self.cam_current_image)
            self.shape.build(data_shape[0], data_shape[1], data_shape[2], data_shape[3])
            self.draw_shape()
            self.apply_new_color(data_shape[4])

        self.timer_count += 1
        if self.timer_count > 5:
            self.iterations_sec.setText(str(1/(time.time() - count)))
            self.timer_count = 0


    @Slot(int, int)
    def hover_position(self, x, y):
        color = QColor(self.cam_current_image.pixel(x, y))
        self.hover_rgb = (color.red(), color.green(), color.blue())

        pix_color = QPixmap(100, 100)
        pix_color.fill(QColor(self.hover_rgb[0], self.hover_rgb[1], self.hover_rgb[2]))
        self.hover_color.setPixmap(pix_color)

    @Slot(int, int)
    def new_color_clicked(self, x, y):
        color = QColor(self.cam_current_image.pixel(x, y))
        self.apply_new_color((color.red(), color.green(), color.blue()))

        new_pos(x, y, self.mid_rgb, self.color_range)
        self.run_tracking = True

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


    @Slot(int, int)
    def apply_camera_size(self, width, height):
        self.graphic_view_picker.setFixedSize(width, height)

    def __del__(self):
        del self.my_threa

    @Slot(int)
    def apply_color_range(self, value):
        self.color_range = value
        self.color_value_label.setText(str(value))
        new_color_range(value)

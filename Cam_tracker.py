from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

last_x = 0
last_y = 0
min_rgb = (0, 0, 0)
max_rgb = (0, 0, 0)
step = 2

def new_pos(x, y, new_min_rgb, new_max_rgb):
    global last_x
    global last_y
    global min_rgb
    global max_rgb

    last_x = x
    last_y = y
    min_rgb = new_min_rgb
    max_rgb = new_max_rgb

def cam_tracker(q_image):
    color = QColor(q_image.pixel(last_x, last_y))
    if not is_pixel_matching(q_image.red(), q_image.green(), q_image.blue()):
        return "lost"

    my_x = last_x
    my_y = last_y
    track = True
    while track:  # CHECK IF IN RANGE
        color = QColor(q_image.pixel(my_x, my_y))
        if not is_pixel_matching(q_image.red(), q_image.green(), q_image.blue()):
            track = False

        my_x -= step


def is_pixel_matching(pixel):
    return min_rgb[0] <= pixel[0] <= max_rgb[0] and min_rgb[1] <= pixel[1] <= max_rgb[1] and min_rgb[2] <= pixel[2] <= max_rgb[2]


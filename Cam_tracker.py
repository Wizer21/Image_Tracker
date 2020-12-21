from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

last_x = 0
last_y = 0
min_rgb = (0, 0, 0)
max_rgb = (0, 0, 0)


step = 2
adaptive_color = (0, 0, 0)
initial_color = (0, 0, 0)
color_iterator = 0
color_range = 0

def new_pos(x, y, mid_rgb, new_color_range):
    global last_x
    global last_y
    global color_iterator
    global color_range
    global adaptive_color
    global initial_color

    last_x = x
    last_y = y
    color_range = new_color_range
    initial_color = mid_rgb

    cal_colors(mid_rgb)

    red = int(min_rgb[0] + (max_rgb[0] - min_rgb[0]) / 2)
    green = int(min_rgb[1] + (max_rgb[1] - min_rgb[1]) / 2)
    blue = int(min_rgb[2] + (max_rgb[2] - min_rgb[2]) / 2)
    adaptive_color = (red, green, blue)

    color_iterator = 0

def cam_tracker(q_image):
    global last_x
    global last_y
    global adaptive_color
    global color_iterator

    cal_colors(adaptive_color)  # Calc min and max color from adaptive_color

    color = QColor(q_image.pixel(last_x, last_y))
    if not is_pixel_matching((color.red(), color.green(), color.blue())):
        # PARCOURIR LA MAP POUR TROUVER UNE FORME AVEC LA DERNIERE COULEUR
        cal_colors(initial_color)  # Try if center is matching initial color
        if not is_pixel_matching((color.red(), color.green(), color.blue())):
            return 0, 0, 0, 0, adaptive_color

    track = True

    left = last_x
    while track:  # CHECK IF IN RANGE
        color = QColor(q_image.pixel(left, last_y))
        if not is_pixel_matching((color.red(), color.green(), color.blue())):
            color = QColor(q_image.pixel(left - step*2, last_y))
            if not is_pixel_matching((color.red(), color.green(), color.blue())):
                break
            else:
                left -= step*2
        left -= step
    left += step

    right = last_x
    while track:  # CHECK IF IN RANGE
        color = QColor(q_image.pixel(right, last_y))
        if not is_pixel_matching((color.red(), color.green(), color.blue())):
            color = QColor(q_image.pixel(right + step*2, last_y))
            if not is_pixel_matching((color.red(), color.green(), color.blue())):
                break
            else:
                right += step*2
        right += step
    right -= step

    top = last_y
    while track:  # CHECK IF IN RANGE
        color = QColor(q_image.pixel(last_x, top))
        if not is_pixel_matching((color.red(), color.green(), color.blue())):
            color = QColor(q_image.pixel(last_x, top - step*2))
            if not is_pixel_matching((color.red(), color.green(), color.blue())):
                break
            else:
                top -= step*2
        top -= step
    top += step

    bot = last_y
    while track:  # CHECK IF IN RANGE
        color = QColor(q_image.pixel(last_x, bot))
        if not is_pixel_matching((color.red(), color.green(), color.blue())):
            color = QColor(q_image.pixel(last_x, bot + step*2))
            if not is_pixel_matching((color.red(), color.green(), color.blue())):
                break
            else:
                bot += step*2
        bot += step
    bot -= step

    last_x = int(left + ((right - left)/2))
    last_y = int(top + ((bot - top)/2))

    adaptive_color = (int(adaptive_color[0] / color_iterator), int(adaptive_color[1] / color_iterator), int(adaptive_color[2] / color_iterator))
    color_iterator = 0

    return top, right, bot, left, adaptive_color


def is_pixel_matching(pixel):
    global adaptive_color
    global color_iterator

    if min_rgb[0] <= pixel[0] <= max_rgb[0] and min_rgb[1] <= pixel[1] <= max_rgb[1] and min_rgb[2] <= pixel[2] <= max_rgb[2]:

        adaptive_color = ((adaptive_color[0] + pixel[0]), adaptive_color[1] + pixel[1], adaptive_color[2] + pixel[2])
        color_iterator += 1

        return True

    return False

def cal_colors(mid_rgb):
    global min_rgb
    global max_rgb

    # Set Min Color
    rgb = [mid_rgb[0], mid_rgb[1], mid_rgb[2]]
    for i in range(len(rgb)):
        rgb[i] -= color_range
        if rgb[i] < 0:
            rgb[i] = 0
    min_rgb = (rgb[0], rgb[1], rgb[2])

    # Set Max Color
    rgb = [mid_rgb[0], mid_rgb[1], mid_rgb[2]]
    for i in range(len(rgb)):
        rgb[i] += color_range
        if 255 < rgb[i]:
            rgb[i] = 255
    max_rgb = (rgb[0], rgb[1], rgb[2])

def new_color_range(new_value):
    global color_range
    color_range = new_value
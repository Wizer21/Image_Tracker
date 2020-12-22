from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

last_x = 0
last_y = 0
min_rgb = (0, 0, 0)
max_rgb = (0, 0, 0)

min_dimeter = 0
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
    global min_dimeter
    last_x = x
    last_y = y
    color_range = new_color_range
    initial_color = mid_rgb
    min_dimeter = step

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
    global min_dimeter

    cal_colors(adaptive_color)  # Calc min and max color from adaptive_color
    define_starter(q_image)

    # Define start positions
    top = [last_x, last_y]
    top_right = [last_x, last_y]
    right = [last_x, last_y]
    bot_right = [last_x, last_y]
    bot = [last_x, last_y]
    bot_left = [last_x, last_y]
    left = [last_x, last_y]
    top_left = [last_x, last_y]

    positions = [top, top_right, right, bot_right, bot, bot_left, left, top_left]
    variations = [[0, -step],
                 [+step, -step],
                 [+step, 0],
                 [+step, +step],
                 [0, +step],
                 [-step, +step],
                 [-step, 0],
                 [-step, -step]]

    track = True
    for i in range(len(positions)):
        while track:
            color = QColor(q_image.pixel(positions[i][0], positions[i][1]))
            if is_pixel_matching((color.red(), color.green(), color.blue())):
                positions[i][0] += variations[i][0]
                positions[i][1] += variations[i][1]
            else:
                color = QColor(q_image.pixel(positions[i][0] + int((variations[i][0] * 2)), positions[i][1] + int((variations[i][1] * 2))))
                if is_pixel_matching((color.red(), color.green(), color.blue())):
                    positions[i][0] += (variations[i][0] * 2)
                    positions[i][1] += (variations[i][1] * 2)
                else:
                    color = QColor(q_image.pixel(positions[i][0] + int((variations[i][0] * 3)), positions[i][1] + int((variations[i][1] * 3))))
                    if is_pixel_matching((color.red(), color.green(), color.blue())):
                        positions[i][0] += (variations[i][0] * 3)
                        positions[i][1] += (variations[i][1] * 3)
                    else:
                        break
        positions[i][0] -= variations[i][0]
        positions[i][1] -= variations[i][1]

    last_x = left[0] + int(((right[0] - left[0])/2))
    last_y = top[1] + int(((bot[1] - top[1])/2))

    if color_iterator != 0:
        adaptive_color = (int(adaptive_color[0] / color_iterator), int(adaptive_color[1] / color_iterator), int(adaptive_color[2] / color_iterator))
    color_iterator = 0

    new_top_left = top_left
    if left[0] < top_left[0]:
        top_left[0] = left[0]
    if top[1] < top_left[1]:
        top_left[1] = top[1]

    new_bot_right = bot_right
    if right[0] > bot_right[0]:
        bot_right[0] = right[0]
    if bot[1] > bot_right[1]:
        bot_right[1] = bot[1]

    if right[0] - left[0] > 10:
        min_dimeter = right[0] - left[0]
    if min_dimeter > bot[1] - top[1] > 10:
        min_dimeter = bot[1] - top[1]
    if min_dimeter > bot_right[0] - top_left[0] > 10:
        min_dimeter = bot_right[0] - top_left[0]
    if min_dimeter > bot_right[1] - top_left[1] > 10:
        min_dimeter = bot_right[1] - top_left[1]

    print("dia" + str(min_dimeter))
    new_width = new_bot_right[0] - new_top_left[0]
    new_height = new_bot_right[1] - new_top_left[1]

    return new_top_left, new_bot_right, new_width, new_height, adaptive_color


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


def define_starter(q_image):
    global last_x
    global last_y
    global min_dimeter

    my_range = min_dimeter

    for y in range(3):
        position_list = [[0, 0],
                         [0, -my_range],
                         [+my_range, -my_range],
                         [+my_range, 0],
                         [+my_range, +my_range],
                         [0, +my_range],
                         [-my_range, +my_range],
                         [-my_range, 0],
                         [-my_range, -my_range]]

        for i in range(len(position_list)):
            color = QColor(q_image.pixel(last_x + position_list[i][0] , last_y + position_list[i][1]))
            if is_pixel_matching((color.red(), color.green(), color.blue())):
                last_x += position_list[i][0]
                last_y += position_list[i][1]
                return

        my_range += min_dimeter
    print("lost")

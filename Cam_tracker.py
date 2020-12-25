from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import time

last_x = 0
last_y = 0
min_rgb = (0, 0, 0)
max_rgb = (0, 0, 0)

min_diameter = 0
step = 4
adaptive_color = (0, 0, 0)
mid_rgb = (0, 0, 0)
color_iterator = 0
color_range = 0
variations = []

red_to_green = [0, 0]
red_to_blue = [0, 0]

max_width = 0
max_height = 0


def new_pos(x, y, new_mid_rgb, newcolor_range, new_width, new_height):
    global last_x
    global last_y
    global color_iterator
    global color_range
    global adaptive_color
    global mid_rgb
    global min_diameter
    global variations
    global max_width
    global max_height

    last_x = x
    last_y = y
    color_range = newcolor_range
    mid_rgb = new_mid_rgb
    min_diameter = step

    adaptive_color = new_mid_rgb
    color_iterator = 1
    cal_colors()
    ini_color()

    variations = [[0, -step],
                 [+step, -step],
                 [+step, 0],
                 [+step, +step],
                 [0, +step],
                 [-step, +step],
                 [-step, 0],
                 [-step, -step]]

    max_width = new_width
    max_height = new_height


def cam_tracker(pixel_map):
    global last_x
    global last_y
    global min_diameter

    cal_colors()  # Calc min and max color from adaptive_color
    define_starter(pixel_map)

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

    track = True
    for i in range(len(positions)):
        while track:
            if validate_pixel(pixel_map, positions[i][1], positions[i][0]):
                positions[i][0] += variations[i][0]
                positions[i][1] += variations[i][1]
            else:
                y = 1
                matched = False
                while y < 10:
                    if validate_pixel(pixel_map, positions[i][1] + (variations[i][1] * y), positions[i][0] + (variations[i][0] * y)):
                        positions[i][0] += (variations[i][0] * y)
                        positions[i][1] += (variations[i][1] * y)
                        y = 10
                        matched = True
                    y += 1
                if not matched:
                    break

        positions[i][0] -= variations[i][0]
        positions[i][1] -= variations[i][1]

    last_x = left[0] + int(((right[0] - left[0])/2))  # NEXT STARTER
    last_y = top[1] + int(((bot[1] - top[1])/2))

    if left[0] > top_left[0]:  # CORNERS TO LARGEST WAY
        top_left[0] = left[0]
    if top[1] > top_left[1]:
        top_left[1] = top[1]

    if right[0] > bot_right[0]:
        bot_right[0] = right[0]
    if bot[1] > bot_right[1]:
        bot_right[1] = bot[1]

    new_diameter = 0
    if bot_right[0] - top_left[0] > 10:  # FIND MIN DIAMETER
        new_diameter = bot_right[0] - top_left[0]
    if new_diameter > bot_right[1] - top_left[1] > 10:
        new_diameter = bot_right[1] - top_left[1]

    print("new" + str(new_diameter))
    print(str(min_diameter))
    print(str(new_diameter - min_diameter))
    if new_diameter > 10:
        min_diameter += (new_diameter - min_diameter) * 0.01

    print("DIAMETER DIAMETER " + str(round(min_diameter)))
    new_width = bot_right[0] - top_left[0]
    new_height = bot_right[1] - top_left[1]

    update_adaptive_color()

    return top_left, bot_right, new_width, new_height, adaptive_color


def is_pixel_matching(pixel):
    global adaptive_color
    global color_iterator

    if min_rgb[0] <= pixel[0] <= max_rgb[0] and min_rgb[1] <= pixel[1] <= max_rgb[1] and min_rgb[2] <= pixel[2] <= max_rgb[2]:

        adaptive_color = (int(adaptive_color[0]) + pixel[0], int(adaptive_color[1]) + pixel[1], int(adaptive_color[2]) + pixel[2])
        color_iterator += 1
        return True

    return False


def update_adaptive_color():
    global adaptive_color
    global color_iterator

    if color_iterator != 0:
        adaptive_color = (round(int(adaptive_color[0] / color_iterator)), round(int(adaptive_color[1] / color_iterator)), round(int(adaptive_color[2] / color_iterator)))
        color_iterator = 1

        # adaptive_red_green = adaptive_color[1] - adaptive_color[0]  # CHECK IF STILL SAME COLOR
        # if not red_to_green[0] < adaptive_red_green < red_to_green[1]:
        #     adaptive_color = (adaptive_color[0], red_to_green[0], adaptive_color[2])
        #
        # adaptive_red_blue = adaptive_color[2] - adaptive_color[0]
        # if not red_to_blue[0] < adaptive_red_blue < red_to_blue[1]:
        #     adaptive_color = (adaptive_color[0], red_to_blue[0], adaptive_color[2])


def cal_colors():
    global min_rgb
    global max_rgb

    # Set Min Color
    rgb = [adaptive_color[0], adaptive_color[1], adaptive_color[2]]
    for i in range(len(rgb)):
        rgb[i] -= int(color_range)
        if rgb[i] < 0:
            rgb[i] = 0
    min_rgb = (rgb[0], rgb[1], rgb[2])

    # Set Max Color
    rgb = [adaptive_color[0], adaptive_color[1], adaptive_color[2]]
    for i in range(len(rgb)):
        rgb[i] += int(color_range)
        if 255 < rgb[i]:
            rgb[i] = 255
    max_rgb = (rgb[0], rgb[1], rgb[2])


def ini_color():
    global red_to_green
    global red_to_blue

    # half_range = round(color_range / 2)
    #
    # red_to_green = [0, int(mid_rgb[1]) - int(mid_rgb[0])]
    # red_to_green[0] = red_to_green[1] - half_range
    # red_to_green[1] = red_to_green[1] + half_range
    #
    # red_to_blue = [0, int(mid_rgb[2]) - int(mid_rgb[0])]
    # red_to_blue[0] = red_to_blue[1] - half_range
    # red_to_blue[1] = red_to_blue[1] + half_range


def new_color_range(new_value):
    global color_range
    color_range = new_value
    ini_color()


def define_starter(pixel_map):
    global last_x
    global last_y
    global min_diameter

    my_range = round(min_diameter)

    if validate_pixel(pixel_map, last_y, last_x):
        return

    for y in range(3):
        position_list = [[0, -my_range],
                         [+my_range, -my_range],
                         [+my_range, 0],
                         [+my_range, +my_range],
                         [0, +my_range],
                         [-my_range, +my_range],
                         [-my_range, 0],
                         [-my_range, -my_range]]

        for i in range(len(position_list)):
            if validate_pixel(pixel_map, last_y + position_list[i][1], last_x + position_list[i][0]):
                last_x += position_list[i][0]
                last_y += position_list[i][1]
                return
            else:
                if validate_pixel(pixel_map, last_y + position_list[i][1] + variations[i][1], last_x + position_list[i][0] + variations[i][0]):
                    last_x += position_list[i][0] + variations[i][0]
                    last_y += position_list[i][1] + variations[i][1]
                    return
                else:
                    if validate_pixel(pixel_map, last_y + position_list[i][1] - variations[i][1], last_x + position_list[i][0] - variations[i][0]):
                        last_x += position_list[i][0] - variations[i][0]
                        last_y += position_list[i][1] - variations[i][1]
                        return

        my_range += round(min_diameter)
    print("lost")


def validate_pixel(pixel_map, y, x):
    try:
        color = pixel_map[y][x]
        return is_pixel_matching((color[0], color[1], color[2]))
    except IndexError:
        print("catched")
        return False

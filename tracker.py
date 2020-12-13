from Shape import *

top_color = (0, 0, 0)
bottom_color = (0, 0, 0)

step = 0

max_height = 0

def start_tracker(newpixel_map, size, newstep, mincolor, maxcolor):
    global max_height
    global bottom_color
    global top_color
    global step

    max_width = size[0]
    max_height = size[1]
    current_width = 0
    current_heigh = 0
    bottom_color = mincolor
    top_color = maxcolor
    step = newstep
    pixel_map = newpixel_map

    list_of_rows = {}
    last_row = []

    justmatched = False
    continue_analysis = True
    start_matching_row = 0

    while continue_analysis:
        if current_width >= max_width:
            current_width = 0
            if len(last_row) != 0:
                list_of_rows[current_heigh] = last_row.copy()
                last_row.clear()
            current_heigh += step
        if current_heigh >= max_height:
            return compile_items(list_of_rows)

        current_pixel_matched = is_pixel_matching(pixel_map[current_width, current_heigh])

        if current_pixel_matched and not justmatched:
            start_matching_row = current_width
            justmatched = True
        elif not current_pixel_matched and justmatched:
            last_row.append([start_matching_row, current_width])
            justmatched = False

        current_width += step


def compile_items(list_of_rows):
    shapes_list = []

    temporary_shapes = []
    height_iterator = 0
    while height_iterator <= max_height:

        if height_iterator in list_of_rows:
            current_row = list_of_rows[height_iterator]
            if len(temporary_shapes) != 0:
                temporary_shapes = micro_compile(current_row, temporary_shapes)

            for i in range(len(current_row)):
                temporary_shapes.append([[list_of_rows[height_iterator][i][0], height_iterator], [list_of_rows[height_iterator][i][1], height_iterator]])
        else:
            if len(temporary_shapes) != 0:
                for i in range(len(temporary_shapes)):
                    shapes_list.append(Shape(temporary_shapes[i]))
                temporary_shapes.clear()

        height_iterator += step

    return shapes_list

def micro_compile(current_row, temporary_shapes):
    for i in range(len(temporary_shapes)):
        for x in range(len(current_row)):
            if temporary_shapes[i][0][0] <= current_row[x][0] <= temporary_shapes[i][1][0] or temporary_shapes[i][0][0] <= current_row[x][1] <= temporary_shapes[i][1][0]:
                temporary_shapes[i].insert(0, current_row[i])
    return temporary_shapes

def is_pixel_matching(pixel):
    return bottom_color[0] <= pixel[0] <= top_color[0] and bottom_color[1] <= pixel[1] <= top_color[1] and bottom_color[2] <= pixel[2] <= top_color[2]





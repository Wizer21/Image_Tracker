from Shape import *
from Temporary_shape import *

top_color = (0, 0, 0)
bottom_color = (0, 0, 0)

step = 0

max_height = 0
shapes_list = []
temporary_shapes = []
splitted_shapes = {}
compiles_shapes = False
checked_range = 0


def start_tracker(newpixel_map, size, newstep, mincolor, maxcolor, new_compiler_value):
    global max_height
    global bottom_color
    global top_color
    global step
    global shapes_list
    global temporary_shapes
    global splitted_shapes
    global compiles_shapes
    global checked_range

    max_width = size[0]
    max_height = size[1]
    current_width = 0
    current_heigh = 0
    bottom_color = mincolor
    top_color = maxcolor
    step = newstep
    pixel_map = newpixel_map

    if new_compiler_value != 0:
        checked_range = step * new_compiler_value
        compiles_shapes = True
    else:
        checked_range = step
        compiles_shapes = False

    list_of_rows = {}
    last_row = []
    shapes_list.clear()
    temporary_shapes.clear()
    splitted_shapes.clear()

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
    global shapes_list
    global temporary_shapes
    global splitted_shapes

    height_iterator = 0
    while height_iterator <= max_height:
        if height_iterator in list_of_rows:  # Si j'ai des valeurs sur la ligne actuelle
            current_row = list_of_rows[height_iterator]
            if len(temporary_shapes) != 0:  # Si j'ai des formes en stock
                micro_compile(current_row, height_iterator)  # Je check si j'ai des matchs
            else:  # Si je n'ai pas de formes en stock, je les crées
                for i in range(len(current_row)):
                    temporary_shapes.append(Temporary_shape([[[list_of_rows[height_iterator][i][0], height_iterator], [list_of_rows[height_iterator][i][1], height_iterator]]]))

        else:
            push_and_close()  # Pousse les entrées, et compiles les formes terminées

        height_iterator += step

    push_and_close()

    if compiles_shapes:
         shape_compiler()

    return shapes_list


def micro_compile(current_row, height_iterator):
    global shapes_list
    global temporary_shapes
    global splitted_shapes

    did_row_matched = []
    for i in range(len(current_row)):
        did_row_matched.append(False)
    find_split_in = {}

    i = 0
    while i < len(temporary_shapes):  # Je regarde dans mes formes en cour de construction
        for z in range(len(temporary_shapes[i].entries)):
            for x in range(len(current_row)):  # Si certaines matches avec la nouvelle row
                if temporary_shapes[i].entries[z][0][0] - checked_range <= current_row[x][0] <= temporary_shapes[i].entries[z][1][0] + checked_range or \
                        temporary_shapes[i].entries[z][0][0] - checked_range <= current_row[x][1] <= temporary_shapes[i].entries[z][1][0] + checked_range or \
                        current_row[x][0] <= temporary_shapes[i].entries[z][0][0] <= current_row[x][1] or \
                        current_row[x][0] <= temporary_shapes[i].entries[z][1][0] <= current_row[x][1]:
                    if x in find_split_in:
                        if find_split_in[x] == i:
                            continue
                        else:
                            if len(temporary_shapes[i].point_list) != 0:
                                temporary_shapes[find_split_in[x]].import_new_list(temporary_shapes[i].point_list)
                                temporary_shapes[find_split_in[x]].import_entries(temporary_shapes[i].entries)
                                del temporary_shapes[i]
                                i -= 1
                    else:
                        temporary_shapes[i].new_entries.append([[current_row[x][0], height_iterator], [current_row[x][1], height_iterator]])  # J'ajoute à la position 0 pour qu'elle devienne la nouvelle clé d'entrée
                        find_split_in[x] = i
                    did_row_matched[x] = True
        i += 1

    push_and_close()  # Pousse les entrées, et compiles les formes terminées
    for i in range(len(did_row_matched)):  # J'ajouter les zone de la row qui n'ont pas match
        if not did_row_matched[i]:
            temporary_shapes.append(Temporary_shape([[[current_row[i][0], height_iterator], [current_row[i][1], height_iterator]]]))


def is_pixel_matching(pixel):
    return bottom_color[0] <= pixel[0] <= top_color[0] and bottom_color[1] <= pixel[1] <= top_color[1] and bottom_color[2] <= pixel[2] <= top_color[2]


def push_and_close():
    i = 0
    while i < len(temporary_shapes):
        if len(temporary_shapes[i].new_entries) != 0:
            temporary_shapes[i].push_entries()
        else:
            temporary_shapes[i].close_entries()
            shapes_list.append(Shape(temporary_shapes[i].point_list))
            del temporary_shapes[i]
            i -= 1
        i += 1


def shape_compiler():
    global shapes_list

    i = 0
    y = 0
    while i < len(shapes_list):
        while y < len(shapes_list):
            if y != i:
                if shapes_list[i].top_left[0] - checked_range < shapes_list[y].top_left[0] < shapes_list[i].bot_right[0] + checked_range or \
                shapes_list[i].top_left[0] - checked_range < shapes_list[y].bot_right[0] < shapes_list[i].bot_right[0] + checked_range and \
                shapes_list[i].top_left[1] - checked_range < shapes_list[y].top_left[1] < shapes_list[i].bot_right[1] + checked_range or \
                shapes_list[i].top_left[1] - checked_range < shapes_list[y].bot_right[1] < shapes_list[i].bot_right[1] + checked_range:
                    shapes_list[i].import_points(shapes_list[y].point_cloud)
                    del shapes_list[y]
                    if i != 0:
                        i -= 1
                    y -= 1
            y += 1
        i += 1
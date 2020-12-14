from Shape import *

top_color = (0, 0, 0)
bottom_color = (0, 0, 0)

step = 0

max_height = 0
shapes_list = []
temporary_shapes = []

def start_tracker(newpixel_map, size, newstep, mincolor, maxcolor):
    global max_height
    global bottom_color
    global top_color
    global step
    global shapes_list
    global temporary_shapes

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
    shapes_list.clear()
    temporary_shapes.clear()

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

    height_iterator = 0
    while height_iterator <= max_height:

        if height_iterator in list_of_rows:  # Si j'ai des valeurs sur la ligne actuelle
            current_row = list_of_rows[height_iterator]
            if len(temporary_shapes) != 0:  # Si j'ai des formes en stock
                micro_compile(current_row, height_iterator)  # Je check si j'ai des matchs
            else:  # Si je n'ai pas de formes en stock, je les crées
                for i in range(len(current_row)):
                    temporary_shapes.append([[[list_of_rows[height_iterator][i][0], height_iterator], [list_of_rows[height_iterator][i][1], height_iterator]]])
        else:  # Si une ligne est complétement vide, je compile toutes les formes
            for i in range(len(temporary_shapes)):
                shapes_list.append(Shape(temporary_shapes[i]))
            temporary_shapes.clear()

        height_iterator += step

    return shapes_list

def micro_compile(current_row, height_iterator):
    global shapes_list
    global temporary_shapes
    trash = []

    shapesize_list = len(temporary_shapes)
    rowsize_list = len(current_row)
    for i in range(shapesize_list):  # Je regarde dans mes formes en cour de construction
        shape_matched = False
        for x in range(rowsize_list):  # Si certaines matches avec la nouvelle row
            if temporary_shapes[i][0][0][0] <= current_row[x][0] <= temporary_shapes[i][0][1][0] or temporary_shapes[i][0][0][0] <= current_row[x][1] <= temporary_shapes[i][0][1][0]:
                temporary_shapes[i].insert(0, [[current_row[x][0], height_iterator], [current_row[x][1], height_iterator]])  # Si j'ai un match j'ajoute à la position 0 afin qu'elle devienne la nouvelle clé d'entrée dans la forme
                trash.append(current_row[x])
                shape_matched = True
        if not shape_matched:  # Si une forme a 0 matches sur cette ligne, je la considère comme finie et je la compile
            shapes_list.append(Shape(temporary_shapes[i]))
            trash.append(temporary_shapes[i])
    for i in trash:
        del i
    for i in current_row:  # Si certaines zones de row n'ont pas match, je crée de nouvelles formes
        temporary_shapes.append([[[i[0], height_iterator], [i[1], height_iterator]]])


def is_pixel_matching(pixel):
    return bottom_color[0] <= pixel[0] <= top_color[0] and bottom_color[1] <= pixel[1] <= top_color[1] and bottom_color[2] <= pixel[2] <= top_color[2]





from Shape import *

top_color = (0, 0, 0)
bottom_color = (0, 0, 0)

step = 0
id = 0

max_height = 0
shapes_list = []
temporary_shapes = []
splitted_shapes = {}

def start_tracker(newpixel_map, size, newstep, mincolor, maxcolor):
    global max_height
    global bottom_color
    global top_color
    global step
    global shapes_list
    global temporary_shapes
    global id
    global splitted_shapes

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
    splitted_shapes.clear()

    id = 0
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
    global id
    global splitted_shapes

    height_iterator = 0
    while height_iterator <= max_height:

        if height_iterator in list_of_rows:  # Si j'ai des valeurs sur la ligne actuelle
            current_row = list_of_rows[height_iterator]
            if len(temporary_shapes) != 0:  # Si j'ai des formes en stock
                micro_compile(current_row, height_iterator)  # Je check si j'ai des matchs
            else:  # Si je n'ai pas de formes en stock, je les crées
                for i in range(len(current_row)):
                    temporary_shapes.append([id, [[list_of_rows[height_iterator][i][0], height_iterator], [list_of_rows[height_iterator][i][1], height_iterator]]])
                    id += 1
        else:  # Si une ligne est complétement vide, je compile toutes les formes
            if len(temporary_shapes) != 0:
                i = 0
                temporary_shapes.reverse()
                while i < len(temporary_shapes):
                    if temporary_shapes[i][0] in splitted_shapes:
                        id_parent = splitted_shapes[temporary_shapes[i][0]]
                        for y in range(len(temporary_shapes)):
                            if temporary_shapes[i][0] == id_parent:
                                parent = temporary_shapes[y]
                        del temporary_shapes[i][0]
                        for y in range(len(temporary_shapes[i])):
                            parent.append(temporary_shapes[i][y])
                        del temporary_shapes[i]
                        i -= 1
                    else:
                        del temporary_shapes[i][0]
                        shapes_list.append(Shape(temporary_shapes[i]))
                    i += 1
                temporary_shapes.clear()

        height_iterator += step

    return shapes_list


def micro_compile(current_row, height_iterator):
    global shapes_list
    global temporary_shapes
    global id
    global splitted_shapes

    did_row_matched = []
    for i in range(len(current_row)):
        did_row_matched.append(False)
    find_split_in = {}
    find_split_out = False

    i = 0
    while i < len(temporary_shapes):  # Je regarde dans mes formes en cour de construction
        find_split_out = False
        for x in range(len(current_row)):  # Si certaines matches avec la nouvelle row
            if temporary_shapes[i][1][0][0] <= current_row[x][0] <= temporary_shapes[i][1][1][0] or \
                temporary_shapes[i][1][0][0] <= current_row[x][1] <= temporary_shapes[i][1][1][0] or \
                    current_row[x][0] <= temporary_shapes[i][1][0][0] <= current_row[x][1] or \
                    current_row[x][0] <= temporary_shapes[i][1][1][0] <= current_row[x][1]:
                if find_split_out:
                    temporary_shapes.append([id, [[current_row[x][0], height_iterator], [current_row[x][1], height_iterator]]])
                    if temporary_shapes[i][0] in splitted_shapes:
                        parent_id = splitted_shapes[temporary_shapes[i][0]]
                        splitted_shapes[id] = parent_id
                    else:
                        splitted_shapes[id] = temporary_shapes[i][0]
                    id += 1
                elif x in find_split_in:
                    del temporary_shapes[i][0]
                    for y in range(len(temporary_shapes[i])):
                        find_split_in[x].append(temporary_shapes[i][y])
                    del temporary_shapes[i]
                    i -= 1
                    find_split_out = True
                else:
                    temporary_shapes[i].insert(1, [[current_row[x][0], height_iterator], [current_row[x][1], height_iterator]])  # J'ajoute à la position 0 pour qu'elle devienne la nouvelle clé d'entrée
                    find_split_in[x] = temporary_shapes[i]
                    find_split_out = True
                did_row_matched[x] = True
        i += 1
    for i in range(len(did_row_matched)):  # J'ajouter les zone de la row qui n'ont pas match
        if did_row_matched[i] == False:
            temporary_shapes.append([id, [[current_row[i][0], height_iterator], [current_row[i][1], height_iterator]]])
            id += 1

def is_pixel_matching(pixel):
    return bottom_color[0] <= pixel[0] <= top_color[0] and bottom_color[1] <= pixel[1] <= top_color[1] and bottom_color[2] <= pixel[2] <= top_color[2]




from Shape import *

current_width = 0
current_heigh = 0

top_color = (0, 0, 0)
bottom_color = (0, 0, 0)

step = 0

lastClockPosition = 0

items_found = []

max_width = 0
max_height = 0

pixel_map = 0

def start_tracker(newpixel_map, size, newstep, mincolor, maxcolor):
    global max_width
    global max_height
    global current_width
    global current_heigh
    global bottom_color
    global top_color
    global step
    global pixel_map

    max_width = size[0]
    max_height = size[1]
    current_width = 0
    current_heigh = 0
    bottom_color = mincolor
    top_color = maxcolor
    step = newstep
    pixel_map = newpixel_map
    items_found.clear()

    # parcour all the map

    nbr_iterations = 0

    continue_analysis = True
    while continue_analysis:
        if current_width >= max_width:
            current_width -= max_width
            current_heigh += step
        if current_heigh >= max_height:
            print("ITERATIONS " + str(nbr_iterations))
            print("ITEMS " + str(len(items_found)))
            return items_found

        pixel = pixel_map[current_width, current_heigh]

        if is_pixel_matching(pixel):
            if not is_already_found([current_width, current_heigh]):  # La forme est elle déjà analysée
                pixel_list = pixel_scanner()  # Si non, J'analyse ma nouvelle forme
                if pixel_list == "item_already_found":
                    current_width += step
                    nbr_iterations += 1
                    continue  # Je me suis retrouvé dans une forme connue durant le parcout
                newshape = Shape(pixel_list)
                if not newshape.isEmpty:
                    items_found.append(newshape)  # la recherche a trouvé moins de deux pixels

        current_width += step
        nbr_iterations += 1


def pixel_scanner():
    orientation = 0

    my_step = step
    current_shape = []
    iterations = 0

    next_pixel = orient_my_pixel(current_width, current_heigh, orientation)
    keep_loop = True
    while keep_loop:  # Si je commence dans le vide
        if not is_pixel_in(next_pixel[0], next_pixel[1]):
            val = border_catched(next_pixel[0], next_pixel[1])
            current_shape.append(val[0])
            next_pixel = [val[1], val[2]]
            next_pixel = orient_my_pixel(next_pixel[0], next_pixel[1], orientation)
            continue

        new_matching_pixel = start_scanning(next_pixel[0], next_pixel[1], orientation)  # Je vais chercher le pixel qui match de la prochaine ligne

        if new_matching_pixel == "item_already_found":  # Objet déjà scanné
            return "item_already_found"
        elif new_matching_pixel == "full":  # First pixel matched
            orientation -= 1
            if orientation == -1:
                orientation = 0
            next_pixel = orient_my_pixel(next_pixel[0], next_pixel[1], orientation)
        elif new_matching_pixel == "void":  # Si je n'ai rien trouvé
            orientation += 1
            if orientation == 4:
                orientation = 0
            next_pixel = orient_my_pixel(next_pixel[0], next_pixel[1], orientation)
        else:
            next_pixel = new_matching_pixel
            current_shape.append(new_matching_pixel)
            next_pixel = orient_my_pixel(new_matching_pixel[0], new_matching_pixel[1], orientation)

        iterations += 1
        if iterations > 1000:
            return current_shape


def orient_my_pixel(checked_width, checked_height, orientation):
    half_step = round(step/2)
    if orientation == 0:
        return [checked_width + 1, checked_height - half_step]
    if orientation == 1:
        return [checked_width + half_step, checked_height + 1]
    if orientation == 2:
        return [checked_width - 1, checked_height + half_step]
    if orientation == 3:
        return [checked_width - half_step, checked_height - 1]


def start_scanning(checked_width, checked_height, orientation):
    try:
        pixel_map[checked_width, checked_height]
    except IndexError:
        print(str(checked_width), str(checked_height))

    if is_pixel_matching(pixel_map[checked_width, checked_height]):
        return "full"

    for i in range(step):
        next_pixel = next_pixel_pos(checked_width, checked_height, orientation)
        if is_pixel_matching(pixel_map[next_pixel[0], next_pixel[1]]):
            if is_already_found([next_pixel[0], next_pixel[1]]):
                return "item_already_found"
            return [next_pixel[0], next_pixel[1]]
        else:
            checked_width = next_pixel[0]
            checked_height = next_pixel[1]

    return "void"


def next_pixel_pos(checked_width, checked_height, orientation):
    if orientation == 0:
        return [checked_width, checked_height + 1]
    if orientation == 1:
        return [checked_width - 1, checked_height]
    if orientation == 2:
        return [checked_width, checked_height - 1]
    if orientation == 3:
        return [checked_width + 1, checked_height]


def is_pixel_matching(pixel):
    return bottom_color[0] <= pixel[0] <= top_color[0] and bottom_color[1] <= pixel[1] <= top_color[1] and bottom_color[2] <= pixel[2] <= top_color[2]


def is_already_found(new_point):
    for i in range(len(items_found)):
        if items_found[i].is_in_range(new_point):
            return True
    return False

def border_catched(current_width, current_heigh):
    if max_width <= current_width:
        current_width == max_width
        path = get_border_path(current_width, current_heigh, "x")
    elif current_width <= 0:
        current_width = 0
        path = get_border_path(current_width, current_heigh, "x")
    elif max_height <= current_heigh:
        current_heigh = max_height
        path = get_border_path(current_width, current_heigh, "y")
    elif current_heigh <= 0:
        current_heigh = 0
        path = get_border_path(current_width, current_heigh, "y")
    else:
        print("Border Error")

    border_values = []
    still_in_shape = True
    while still_in_shape:
        current_width += path[0]
        current_heigh += path[1]
        if not is_pixel_in(current_width, current_heigh):
            test = 0
        if not is_pixel_matching(pixel_map[current_width, current_heigh]):
            current_width -= path[0]
            current_heigh -= path[1]
            return [border_values, current_width, current_heigh]

        border_values.append([current_width, current_heigh])


def get_border_path(x, y, border):
    if border == "x":
        if is_pixel_in(x + 1, y):
            if is_pixel_matching(pixel_map[x + step/2, y]):
                return  (1, 0)
        if is_pixel_in(x - 1, y):
            if is_pixel_matching(pixel_map[x - step/2, y]):
                return  (-1, 0)
    if border == "y":
        if is_pixel_in(x, y + 1):
            if is_pixel_matching(pixel_map[x, y + step/2]):
                return  (0, 1)
        if is_pixel_in(x, y - 1):
            if is_pixel_matching(pixel_map[x, y - step/2]):
                return  (0, -1)
    print(str(x), str(y))
    if border == "x":
        if is_pixel_in(x + 1, y):
            if is_pixel_matching(pixel_map[x + step/2, y]):
                return  (1, 0)
        if is_pixel_in(x - 1, y):
            if is_pixel_matching(pixel_map[x - step/2, y]):
                return  (-1, 0)
    if border == "y":
        if is_pixel_in(x, y + 1):
            if is_pixel_matching(pixel_map[x, y + step/2]):
                return  (0, 1)
        if is_pixel_in(x, y - 1):
            if is_pixel_matching(pixel_map[x, y - step/2]):
                return  (0, -1)


def is_pixel_in(x, y):
    return 0 <= x <= max_width and 0 <= y <= max_height


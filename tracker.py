from Shape import *

current_width = 0
current_heigh = 0

top_color = (0, 0, 0)
bottom_color = (0, 0, 0)

step = 0

lastClockPosition = 0

items_found = []


def start_tracker(pixel_map, size, newstep, mincolor, maxcolor):
    max_width = size[0]
    max_height = size[1]

    global current_width
    current_width = 0
    global current_heigh
    current_heigh = 0

    global bottom_color
    bottom_color = mincolor
    global top_color
    top_color = maxcolor

    global step
    step = newstep

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
                pixel_list = pixel_scanner(pixel_map)  # Si non, J'analyse ma nouvelle forme
                if pixel_list == "item_already_found":
                    current_width += step
                    nbr_iterations += 1
                    continue  # Je me suis retrouvé dans une forme connue durant le parcout
                newshape = Shape(pixel_list)
                if not newshape.isEmpty:
                    items_found.append(newshape)  # la recherche a trouvé moins de deux pixels

        current_width += step
        nbr_iterations += 1


def pixel_scanner(pixel_map):
    orientation = 0

    my_step = step
    current_shape = []
    iterations = 0
    keep_loop = True

    next_pixel = orient_my_pixel(current_width, current_heigh, orientation)
    while keep_loop:  # Si je commence dans le vide
        new_matching_pixel = start_scanning(next_pixel[0], next_pixel[1], orientation, pixel_map)  # Je vais chercher le pixel qui match de la prochaine ligne

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
        if iterations > 10000:
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


def start_scanning(checked_width, checked_height, orientation, pixel_map):
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


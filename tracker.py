from Shape import *

current_width = 0
current_heigh = 0

top_color = (0, 0, 0)
bottom_color = (0, 0, 0)

step = 0

lastClockPosition = 0

items_found = []


def start_tracker(pixel_map, size, newstep, color_to_found):
    max_width = size[0]
    max_height = size[1]

    global current_width
    current_width = 0
    global current_heigh
    current_heigh = 0

    global top_color
    top_color = (0, 255, 120)
    global bottom_color
    bottom_color = (0, 225, 90)

    global step
    step = newstep

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
                pixel_list = color_matched(pixel_map)  # Si non, J'analyse ma nouvelle forme
                if pixel_list == "item_already_found":
                    current_width += step
                    nbr_iterations += 1
                    continue  # Je me suis retrouvé dans une forme connue durant le parcout
                newshape = Shape(pixel_list)
                if not newshape.isEmpty:
                    items_found.append(newshape)  # la recherche a trouvé moins de deux pixels

        current_width += step
        nbr_iterations += 1


def color_matched(pixel_map):
    my_range = step
    pos_width = current_width
    pos_heigh = current_heigh

    iterations = 0
    current_shape = []
    still_in_shape = True
    while still_in_shape:
        val = check_nearby_pixels(pos_width, pos_heigh, pixel_map, my_range)

        if val == "not_found":
            my_big_range = round(my_range * 2)
            val = check_nearby_pixels(pos_width, pos_heigh, pixel_map, my_big_range)
            if val == "not_found":
                my_big_range = round(my_range * 3)
                val = check_nearby_pixels(pos_width, pos_heigh, pixel_map, my_big_range)
                if val == "not_found":
                    return current_shape

        if val == "item_already_found":
            return "item_already_found"

        print(str(val))
        print(str(iterations))
        pos_width = val[0]
        pos_heigh = val[1]
        current_shape.append(val)

        iterations += 1
        if iterations > 500:
            return current_shape


def check_nearby_pixels(checked_width, checked_height, pixel_map, my_range):
    global lastClockPosition

    low_range = round(my_range * 0.1)
    half_range = round(my_range * 0.6)

    nearby_pixels = [[checked_width, checked_height - my_range],
                     [checked_width + (low_range * 2), checked_height - (my_range - low_range)],
                     [checked_width + half_range, checked_height - half_range],
                     [checked_width + (my_range - low_range), checked_height - (low_range * 2)],
                     [checked_width + my_range, checked_height],
                     [checked_width + (my_range - low_range), checked_height + (low_range * 2)],
                     [checked_width + half_range, checked_height + half_range],
                     [checked_width + (low_range * 2), checked_height + (my_range - low_range)],
                     [checked_width, checked_height + my_range],
                     [checked_width - (low_range * 2), checked_height + (my_range - low_range)],
                     [checked_width - half_range, checked_height + half_range],
                     [checked_width - (my_range - low_range), checked_height + (low_range * 2)],
                     [checked_width - my_range, checked_height],
                     [checked_width - (my_range - low_range), checked_height - (low_range * 2)],
                     [checked_width - half_range, checked_height - half_range],
                     [checked_width - (low_range * 2), checked_height - (my_range - low_range)],
                     ]

    where_out = False
    clock_path = 0
    current_clock = lastClockPosition - 2
    if current_clock < 0:
        keep = current_clock
        current_clock = 16 + current_clock

    while clock_path < 20:
        if where_out:
            if is_pixel_matching(pixel_map[nearby_pixels[current_clock][0], nearby_pixels[current_clock][1]]):
                lastClockPosition = current_clock
                if is_already_found(nearby_pixels[current_clock]):  # Regarde que je n'arrive pas dans une forme connue, durant le parcourt
                    return "item_already_found"
                return nearby_pixels[current_clock]

        if not is_pixel_matching(pixel_map[nearby_pixels[current_clock][0], nearby_pixels[current_clock][1]]):
            where_out = True

        clock_path += 1
        current_clock += 1
        if current_clock == 16:
            current_clock = 0

    return "not_found"


def is_pixel_matching(pixel):
    return bottom_color <= pixel <= top_color


def is_already_found(new_point):
    for i in range(len(items_found)):
        if items_found[i].is_in_range(new_point):
            return True
    return False


current_width = 0
current_heigh = 0

top_color = (0, 0, 0)
bottom_color = (0, 0, 0)

step = 0

lastClockPosition = 0


def get_position(pixel_map, size, newstep, color_to_found):
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

    items_found = []
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
            newshape = color_matched(pixel_map)
            if len(newshape) != 0:
                items_found.append(newshape)

        current_width += step
        nbr_iterations += 1


def color_matched(pixel_map):

    still_matching = True

    my_range = round(step/2)
    pos_width = current_width
    pos_heigh = current_heigh

    iterations = 0
    drawing_shape = []
    still_in_shape = True
    while still_in_shape:
        val = check_nearby_pixels(pos_width, pos_heigh, pixel_map, my_range)

        if val == "not_found":
            my_big_range = round(my_range*2)
            val = check_nearby_pixels(pos_width, pos_heigh, pixel_map, my_big_range)
            if val == "not_found":
                still_in_shape = False

        if val != "not_found":
            pos_width = val[0]
            pos_heigh = val[1]
            drawing_shape.append(val)

        iterations += 1
        if iterations > 50:
            still_in_shape = False

    # print("SHAPE" + str(drawing_shape))
    return drawing_shape


def check_nearby_pixels(checked_width, checked_height, pixel_map, my_range):
    global lastClockPosition

    half_range = round(my_range/2)
    nearby_pixels = [[checked_width, checked_height + my_range],
                     [checked_width + half_range, checked_height + half_range],
                     [checked_width + my_range, checked_height],
                     [checked_width + half_range, checked_height - half_range],
                     [checked_width, checked_height - my_range],
                     [checked_width - half_range, checked_height - half_range],
                     [checked_width - my_range, checked_height],
                     [checked_width - half_range, checked_height + half_range]]

    where_out = False
    iterations = 0
    current_clock = lastClockPosition - 2
    if current_clock < 0:
        keep = current_clock
        current_clock = 8 + current_clock

    while iterations < 10:
        if where_out:
            if is_pixel_matching(pixel_map[nearby_pixels[current_clock][0], nearby_pixels[current_clock][1]]):
                lastClockPosition = current_clock
                return nearby_pixels[current_clock]
        if not is_pixel_matching(pixel_map[nearby_pixels[current_clock][0], nearby_pixels[current_clock][1]]):
            where_out = True

        iterations += 1
        current_clock += 1
        if current_clock == 8:
            current_clock = 0

    return "not_found"


def is_pixel_matching(pixel):
    return bottom_color <= pixel <= top_color

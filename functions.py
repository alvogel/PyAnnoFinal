import math


# returns the minimal bounding box of the surface for colors which are not black(background)

def find_bounding_box(s):

    w = s.get_width()
    h = s.get_height()

    # Find bounding box
    # find min x
    min_x = 100
    for x in range(100):
        x_free = True
        for y in range(h):
            if s.get_at((x, y)) == (255, 255, 255, 255):
                x_free = False
                break

        if x_free == False:
            min_x = x
            break

    # find min y
    min_y = 100
    for y in range(100):
        y_free = True
        for x in range(min_x, w):
            if s.get_at((x, y)) == (255, 255, 255, 255):
                y_free = False
                break

        if y_free == False:
            min_y = y
            break

    # find max x
    max_x = 100
    for x in range(w - 1, 100, -1):
        x_free = True
        for y in range(min_y, h):
            if s.get_at((x, y)) == (255, 255, 255, 255):
                x_free = False
                break

        if x_free == False:
            max_x = x
            break

    # find min y
    max_y = 100
    for y in range(h - 1, 100, -1):
        y_free = True
        for x in range(min_x, max_x):
            if s.get_at((x, y)) == (255, 255, 255, 255):
                y_free = False
                break

        if y_free == False:
            max_y = y
            break

    return (min_x, min_y, max_x-min_x,max_y-min_y)


# sigmoid function

def sigmoid(x):
    return 1 / (1 + math.e**-x)


# derivation og sigmoid function

def dsigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))
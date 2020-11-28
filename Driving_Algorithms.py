import time
import pyautogui
import math

def point_to_line_dist(point, line):
    a = point[0] - line[0]
    b = point[1] - line[1]
    c = line[2] - line[0]
    d = line[3] - line[1]

    dot = a * c + b * d
    len_sq = c * c + d * d

    param = dot / len_sq

    if param < 0:
        xx = line[0]
        yy = line[1]

    elif param > 1:
        xx = line[2]
        yy = line[3]

    else:
        xx = line[0] + param * c
        yy = line[1] + param * d

    dx = point[0] - xx
    dy = point[1] - yy
    return math.sqrt(dx * dx + dy * dy)

def drive_lane_intersect(lanes, screen_width):
    """This algorithm is an attempt to drive the car based on predetermined instructions.

    The method used here is to move the car such that the middle (x-coordinate) of the
    screen is aligned with the intersection of the projection of the two lane lines.
    """

    x1, y1, x2, y2 = 0, 1, 2, 3

    center_screen = screen_width // 2

    if len(lanes) == 2 and any({(line[3] - line[1]) / (line[2] - line[0]) > 0 for line in lanes}) \
            and any({(line[3] - line[1]) / (line[2] - line[0]) < 0 for line in lanes}):

        line_1, line_2 = lanes[0], lanes[1]

        intersect_x = (((line_1[x2] * line_1[y1] - line_1[x1] * line_1[y2]) * (line_2[x2] - line_2[x1])) \
                       - ((line_2[x2] * line_2[y1] - line_2[x1] * line_2[y2]) * (line_1[x2] - line_1[x1]))) \
                      / ((line_1[x2] - line_1[x1]) * (line_2[y2] - line_2[y1]) - (line_2[x2] - line_2[x1]) * (
                    line_1[y2] - line_1[y1]))


        if center_screen > intersect_x:
            pyautogui.keyDown('a')
            time.sleep(0.01)
            pyautogui.keyUp('a')
        elif center_screen < intersect_x:
            pyautogui.keyDown('d')
            time.sleep(0.01)
            pyautogui.keyUp('d')

    else:
        line = lanes[0]
        if (line[3] - line[1]) / (line[2] - line[0]) < 0:
            pyautogui.keyDown('d')
            time.sleep(0.01)
            pyautogui.keyUp('d')
        else:
            pyautogui.keyDown('a')
            time.sleep(0.01)
            pyautogui.keyUp('a')


def drive_max_dist(lanes, screen_size):
    """This algorithm is an attempt to drive the car based on predetermined instructions.

    The method used here is moving the car such that it tries to keep the same distance between
    both lanes.
    """

    if len(lanes) == 2 and any({(line[3] - line[1]) / (line[2] - line[0]) > 0 for line in lanes}) \
            and any({(line[3] - line[1]) / (line[2] - line[0]) < 0 for line in lanes}):

        if (lanes[0][3] - lanes[0][1]) / (lanes[0][2] - lanes[0][0]) < 0:
            left_lane = lanes[0]
            right_lane = lanes[1]

        else:
            left_lane = lanes[1]
            right_lane = lanes[0]

        # TODO: DO NOT HARDCODE THIS. MAKE THIS FUNCTION TAKE SCREEN SIZE PARAMETER
        car = (screen_size[0] // 2, screen_size[1] - 200)
        left_dist = point_to_line_dist(car, left_lane)
        right_dist = point_to_line_dist(car, right_lane)

        if left_dist < right_dist:
            pyautogui.keyDown('d')
            time.sleep(0.01)
            pyautogui.keyUp('d')
        else:
            pyautogui.keyDown('a')
            time.sleep(0.01)
            pyautogui.keyUp('a')

    #  TODO: need smarter intelliegnce for when only 1 line
    else:
        line = lanes[0]
        if (line[3] - line[1]) / (line[2] - line[0]) < 0:
            pyautogui.keyDown('d')
            time.sleep(0.01)
            pyautogui.keyUp('d')
        else:
            pyautogui.keyDown('a')
            time.sleep(0.01)
            pyautogui.keyUp('a')

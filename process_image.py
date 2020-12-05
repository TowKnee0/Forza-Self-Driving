import cv2
import numpy as np
import algorithms


def mask_region(screen, vertices):
    """Returns region of interest based on given vertices.

    Note: screen should be processed already using Canny edge detection.
    """

    # Creates a mask of 0's. The pixels in the region of interest are filled
    # to white. Finally bitwise_and returns white when both mask and screen are
    # white (per pixel) and black otherwise.
    mask = np.zeros_like(screen)
    cv2.fillPoly(mask, vertices, 255)
    np.set_printoptions(threshold=np.inf)

    return cv2.bitwise_and(screen, mask)


def lane_lines(screen):
    """Takes in a screen as input and performs a hough transform on the image. The hough
    lines are then drawn on top of the input image.

    Note: screen should be at least edge detection processed. Better if screen is passed
          after region of interest is applied to edge detection.
    """
    lines_mess = cv2.HoughLinesP(screen, rho=1, theta=np.pi / 180, threshold=180, minLineLength=60, maxLineGap=1)

    # Note: lines is in the form [[[here]], [[here]]...]

    if lines_mess is not None:
        sorter = algorithms.HoughCluster()
        lines = sorter.process_lines(lines_mess, screen)
        # temp = lines
        temp = {}

        # only return 2 lines
        if lines is not None:
            max_slope = 0
            min_slope = 0
            for line in lines:
                slope = (line[3] - line[1]) / (line[2] - line[0])
                if slope > max_slope:
                    max_slope = slope
                    temp['max'] = line

                elif slope < min_slope:
                    min_slope = slope
                    temp['min'] = line

        if len(temp) > 0:
            return [temp[key] for key in temp]


def process_image(screen):
    """ Takes in the screenshot, applies edge detection and mask and blur
    then returns the new screen.
    """
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_screen, threshold1=200, threshold2=350)

    vertices = np.array(
        [[10, 450], [400, 375], [650, 375], [950, 450], [950, 700], [600, 700], [550, 450], [400, 450], [300, 700],
         [10, 700]], dtype=np.int32)

    masked = mask_region(edges, [vertices])
    blur = cv2.GaussianBlur(masked, (3, 3), 0)

    return blur

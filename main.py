import cv2
import numpy as np
from PIL import ImageGrab
import Algorithms
import Driving_Algorithms


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
    lines_mess = cv2.HoughLinesP(screen, rho=1, theta=np.pi/180, threshold=180, minLineLength=60, maxLineGap=5)

    # Note: lines is in the form [[[here]], [[here]]...]

    if lines_mess is not None:
        sorter = Algorithms.HoughCluster()
        lines = sorter.process_lines(lines_mess, screen)
        temp = lines

        # only return 2 lines
        if len(lines) > 2:
            temp = []
            max_slope = 0.1
            min_slope = - 0.1
            for line in lines:
                slope = (line[3] - line[1]) / (line[2] - line[0])
                if slope > max_slope:
                    max_slope = slope
                    if len(temp) == 2:
                        temp.pop()
                    temp.append(line)
                elif slope < min_slope:
                    min_slope = slope
                    if len(temp) == 2:
                        temp.pop(0)
                    temp.insert(0, line)

        return temp


def process_image(screen):
    """ Takes in the screenshot, applies edge detection and mask and blur
    then returns the new screen.
    """
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_screen, threshold1=200, threshold2=300)

    vertices = np.array([[10, 450], [400, 375], [650, 375], [950, 450], [950, 700], [750, 700], [600, 450], [400, 450], [250, 700], [10, 700]], dtype=np.int32)

    masked = mask_region(edges, [vertices])
    blur = cv2.GaussianBlur(masked, (3, 3), 0)

    # lanes = lane_lines(blur)
    #
    # if lanes is not None:
    #     if len(lanes) == 2:
    #         Driving_Algorithms.drive_max_dist(lanes)
    #
    #     for line in lanes:
    #         cv2.line(blur, (line[0], line[1]), (line[2], line[3]), (255, 0, 255), 10)

    return blur


while True:
    # store raw pixel data into np array
    screen = np.array(ImageGrab.grab(bbox=(0, 100, 950, 800)))

    processed = process_image(screen)
    lanes = lane_lines(processed)
    if lanes is not None:
        Driving_Algorithms.drive_max_dist(lanes, (950, 800))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

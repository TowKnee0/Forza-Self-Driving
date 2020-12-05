import cv2
import numpy as np
import driving_algorithms
import screen_grab
import time
import process_image


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
    lines_mess = cv2.HoughLinesP(screen, rho=1, theta=np.pi/180, threshold=180, minLineLength=60, maxLineGap=1)

    # Note: lines is in the form [[[here]], [[here]]...]

    if lines_mess is not None:
        #
        # for line in lines_mess:
        #     line = line[0]
        #     cv2.line(screen, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 1)

        sorter = Algorithms.HoughCluster()
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


pressed = False
last_time = time.time()
while True:
    # store raw pixel data into np array
    screen = np.array(screen_grab.grab_screen(region=(0, 100, 950, 800)))

    processed = process_image.process_image(screen)
    lanes = process_image.lane_lines(processed)

    if lanes is not None:
        pressed = driving_algorithms.drive_max_dist(lanes, (950, 800), pressed)

    #     for line in lanes:
    #         cv2.line(processed, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 5)
    # cv2.imshow('test', processed)

    print(f'Loop took {time.time() - last_time} seconds')
    last_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

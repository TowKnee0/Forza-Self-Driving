import cv2
import numpy as np
import Driving_Algorithms
import screen_grab
import time
import process_image
from typing import Tuple, List


pressed = False
last_time = time.time()
while True:
    # store raw pixel data into np array
    screen = np.array(screen_grab.grab_screen(region=(0, 100, 950, 800)))

    processed = process_image.process_image(screen)
    lanes = process_image.lane_lines(processed)

    if lanes is not None:
        pressed = Driving_Algorithms.drive_max_dist(lanes, (950, 800), pressed)

    #     for line in lanes:
    #         cv2.line(processed, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 5)
    # cv2.imshow('test', processed)

    # print(f'Loop took {time.time() - last_time} seconds')
    # last_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

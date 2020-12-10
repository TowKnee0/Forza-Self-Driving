import screen_grab
import process_image
import numpy as np
import win32api
import time
from typing import List


def encoded(key: List[str]) -> List[int]:
    """One hot encodes the keys to prep for neural network.

    """
    if 'A' in key:
        return [1, 0, 0]
    elif 'B' in key:
        return [0, 1, 0]
    else:
        return [0, 0, 1]


def key_check() -> List[str]:
    """Checks and return which keys are currently being pressed.

    """
    keys = []
    for key in keyList:
        if win32api.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys


keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    keyList.append(char)


if __name__ == '__main__':

    inplay = True
    data = []
    time.sleep(5)
    while inplay:
        screen = np.array(screen_grab.grab_screen(region=(0, 100, 950, 800)))

        processed = process_image.process_image(screen)
        lanes = process_image.lane_lines(processed)

        key = key_check()
        if ' ' in key:
            inplay = False
            break

        if lanes is not None:
            one_hot = encoded(key_check())
            data.append([lanes, one_hot])

            if len(data) % 500 == 0:
                temp = list(np.load('data.npy', allow_pickle=True))
                print(f'Length: {len(temp)}')
                temp.extend(data)
                np.save('data.npy', temp, allow_pickle=True)
                data = []

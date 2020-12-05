from pynput import keyboard

# One hot encoded
A = [1, 0, 0]
D = [0, 1, 0]
NOTHING = [0, 0, 1]



temp = []

def on_press(key):
    try:
        global temp
        if key.char == 'a':
            # print(A)
            temp.append(A)
        elif key.char == 'd':
            # print(D)
            temp.append(D)
        elif key.char == 'x':
            listener.stop()
        else:
            # print(NOTHING)
            temp.append(NOTHING)
        print(temp)
    except Exception as e:
        print(e)


def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released


# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press)
listener.start()

print('hellow world')

import numpy as np
import cv2
from pynput.mouse import Controller
from colormap import rgb2hex
from mss import mss

controller = Controller()

capture = 'c'  # capture key
w = h = 300
window = np.zeros((w, h, 4), np.uint8)
window *= 255


def main():
    while True:
        # when capture key is pressed, take a screenshot at the mouse position
        if cv2.waitKey(1) == ord(capture):
            x, y = controller.position
            with mss() as sct:
                raw_pixels = sct.grab({"top": y, "left": x, "width": 1, "height": 1})
                screen = np.array(raw_pixels)

                rgb = list(screen[0][0])[:-1]  # removes the weird last element
                rgb = rgb[::-1]  # flips from BGR to RGB
                hex_value = rgb2hex(rgb[0], rgb[1], rgb[2])

                print(f'{rgb} - {hex_value}')

                rgb = list(map(int, rgb))
                cv2.rectangle(window, (0, 0), (w, h), rgb[::-1], -1)  # color is reverted back to BGR as cv2 uses BGR

                # text color changes to either black or white based on the background color to maintain readability
                text_color = (255, 255, 255) if np.average(rgb, axis=0) < 128 else (0, 0, 0)
                cv2.putText(window, f'Press {capture}', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 1)
                cv2.putText(window, str(rgb), (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 1)
                cv2.putText(window, str(hex_value), (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 1)


        cv2.imshow("Color Picker", window)


main()

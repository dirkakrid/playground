import micropython
from machine import Pin
from neopixel import NeoPixel
from button import Button
import time

micropython.alloc_emergency_exception_buf(100)
b = Button(0, max_clicks=3)
np = NeoPixel(Pin(15, Pin.OUT), 3)


def fill_np(pixel, clicks):
    for i, x in enumerate(clicks):
        if x == -1:
            color = (0, 0, 0)
        elif x < 300:
            color = (100, 0, 0)
        elif x > 1500:
            color = (0, 0, 100)
        else:
            color = (0, 100, 0)
        pixel[i] = color
    pixel.write()


while True:
    if b.ready():
        fill_np(np, b.clicks)
        time.sleep(1.0)
        np.fill((0, 0, 0))
        np.write()
    else:
        time.sleep(0.1)

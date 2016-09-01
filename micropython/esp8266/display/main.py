#!/usr/bin/env python3
import time
from machine import Pin, freq, reset, I2C, Timer
from ssd1306 import SSD1306_I2C
import urandom

freq(160000000)

_ = reset
disp = SSD1306_I2C(64, 48, I2C(Pin(5), Pin(4)))


def display_bitmap(display, file):
    with open(file) as f:
        for y, line in enumerate(f):
            for x, pix in enumerate(line.strip()):
                display.pixel(x, y, int(pix))
    display.show()

IMAGES = [
    "logo.ascii",
    "hc.ascii",
    "pony.ascii",
    "py.ascii",
    "icode.ascii",
]


def change_bitmap():
    idx = urandom.getrandbits(4) % len(IMAGES)
    display_bitmap(disp, IMAGES[idx])

t = Timer(-1)
t.init(period=10000, mode=Timer.PERIODIC, callback=lambda t: change_bitmap())

button = Pin(0, mode=Pin.IN, pull=Pin.PULL_UP)
display_bitmap(disp, IMAGES[0])
while True:
    time.sleep_ms(10)
    if button.value() == 0:
        change_bitmap()

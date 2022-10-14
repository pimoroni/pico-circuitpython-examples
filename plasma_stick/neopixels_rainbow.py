# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
NeoPixel example for Pico. Displays a rainbow on the NeoPixels.
REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP15.
"""
import time
import board
from rainbowio import colorwheel
import neopixel

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 50

pixels = neopixel.NeoPixel(board.GP15, num_pixels, auto_write=False)
pixels.brightness = 0.5


def rainbow(speed):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(speed)


while True:
    rainbow(0)
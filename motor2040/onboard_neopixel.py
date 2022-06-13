# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Internal RGB LED red, green, blue example"""
import time
import board

import neopixel
led = neopixel.NeoPixel(board.LED_DATA, board.NUM_LEDS)

led.brightness = 0.3

while True:
    for i in range(board.NUM_LEDS):
        led[i] = (255, 0, 0)
        time.sleep(0.5)

    for i in range(board.NUM_LEDS):
        led[i] = (0, 255, 0)
        time.sleep(0.5)

    for i in range(board.NUM_LEDS):
        led[i] = (0, 0, 255)
        time.sleep(0.5)

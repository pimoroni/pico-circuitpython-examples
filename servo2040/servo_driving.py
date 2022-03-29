# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Servo standard servo example"""
import time
import board
import pwmio
from adafruit_motor import servo

# Specify which servo pins to use.
pins = [ board.SERVO_1, board.SERVO_2, board.SERVO_3, board.SERVO_4 ]

# Create a servo object for each pin
servos = [ servo.Servo(pwmio.PWMOut(pin, duty_cycle=2 ** 15, frequency=50)) for pin in pins]

while True:
    for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
        for i in range(len(pins)):
            servos[i].angle = angle
        time.sleep(0.05)
    for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
        for i in range(len(pins)):
            servos[i].angle = angle
        time.sleep(0.05)
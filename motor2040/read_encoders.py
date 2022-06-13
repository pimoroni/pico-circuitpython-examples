# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import rotaryio

# Encoder constants
GEAR_RATIO = 50                     # The gear ratio of the motor
COUNTS_PER_REV = 12 * GEAR_RATIO    # The counts per revolution of the motor's output shaft
ENCODER_NAMES = ["A", "B", "C", "D"]

# Create a digitalinout object for the user switch
user_sw = digitalio.DigitalInOut(board.USER_SW)
user_sw.direction = digitalio.Direction.INPUT
user_sw.pull = digitalio.Pull.UP

# Create the encoder objects
enc_a = rotaryio.IncrementalEncoder(board.ENCODER_A_B, board.ENCODER_A_A, divisor=1)
enc_b = rotaryio.IncrementalEncoder(board.ENCODER_B_B, board.ENCODER_B_A, divisor=1)
enc_c = rotaryio.IncrementalEncoder(board.ENCODER_C_B, board.ENCODER_C_A, divisor=1)
enc_d = rotaryio.IncrementalEncoder(board.ENCODER_D_B, board.ENCODER_D_A, divisor=1)
encoders = [enc_a, enc_b, enc_c, enc_d]


def button_pressed():
    return not user_sw.value


def to_degrees(position):
    return (position * 360.0) / COUNTS_PER_REV


# Run until the user switch is pressed
while not button_pressed():

    # Print out the angle of each encoder
    for i in range(board.NUM_ENCODERS):
        print(ENCODER_NAMES[i], "=", to_degrees(encoders[i].position), end=", ")
    print()

    time.sleep(0.1)

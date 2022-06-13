# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import board
import digitalio
import rotaryio

# Pins of the motor encoder to read
CHANNEL_A = board.ENCODER_A_A
CHANNEL_B = board.ENCODER_A_B

# Encoder constants
REVERSED = True     # Whether to reverse the counting direction (set to True if using MMME)

# Create a digitalinout object for the user switch
user_sw = digitalio.DigitalInOut(board.USER_SW)
user_sw.direction = digitalio.Direction.INPUT
user_sw.pull = digitalio.Pull.UP

# Create the encoder object
if REVERSED:
    encoder = rotaryio.IncrementalEncoder(CHANNEL_B, CHANNEL_A, divisor=1)
else:
    encoder = rotaryio.IncrementalEncoder(CHANNEL_A, CHANNEL_B, divisor=1)


last_position = None


def button_pressed():
    return not user_sw.value


# Run until the user switch is pressed
while not button_pressed():
    position = encoder.position
    if last_position is None or position != last_position:
        print(position)
    last_position = position

# SPDX-License-Identifier: MIT

import time
import board
import pwmio
import digitalio
from adafruit_motor import motor

# Pins of the motor to drive
MOTOR_P = board.MOTOR_A_P
MOTOR_N = board.MOTOR_A_N

# Motor constants
FREQUENCY = 25000               # Chose a frequency above human hearing
DECAY_MODE = motor.SLOW_DECAY   # The decay mode affects how the motor
                                # responds, with SLOW_DECAY having improved spin
                                # threshold and speed-to-throttle linearity

# Create a digitalinout object for the user switch
user_sw = digitalio.DigitalInOut(board.USER_SW)
user_sw.direction = digitalio.Direction.INPUT
user_sw.pull = digitalio.Pull.UP

# Create the pwm and motor objects
pwm_p = pwmio.PWMOut(MOTOR_P, frequency=FREQUENCY)
pwm_n = pwmio.PWMOut(MOTOR_N, frequency=FREQUENCY)
mot = motor.DCMotor(pwm_p, pwm_n)

# Set the motor decay modes (if unset the default will be FAST_DECAY)
mot.decay_mode = DECAY_MODE


def button_pressed():
    return not user_sw.value


# Run the motor sequence
while True:
    # Forward slow
    mot.throttle = 0.5
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Stop
    mot.throttle = 0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Forward fast
    mot.throttle = 1.0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Spin freely
    mot.throttle = None
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Backwards slow
    mot.throttle = -0.5
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Stop
    mot.throttle = 0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Backwards fast
    mot.throttle = -1.0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Spin freely
    mot.throttle = None
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

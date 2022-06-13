# SPDX-License-Identifier: MIT

import time
import board
import pwmio
import digitalio
from adafruit_motor import motor

# Pin names for the Pico Motor Shim
BUTTON_A = board.GP2
MOTOR_1_P = board.GP6
MOTOR_1_N = board.GP7
MOTOR_2_P = board.GP27
MOTOR_2_N = board.GP26

# Motor constants
FREQUENCY = 25000               # Chose a frequency above human hearing
DECAY_MODE = motor.SLOW_DECAY   # The decay mode affects how the motor
                                # responds, with SLOW_DECAY having improved spin
                                # threshold and speed-to-throttle linearity

# Create a digitalinout object for the button
button_a = digitalio.DigitalInOut(BUTTON_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

# Create a digitalinout object for the Pico's LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Create the pwm and motor objects
pwm_1p = pwmio.PWMOut(MOTOR_1_P, frequency=FREQUENCY)
pwm_1n = pwmio.PWMOut(MOTOR_1_N, frequency=FREQUENCY)
motor1 = motor.DCMotor(pwm_1p, pwm_1n)

pwm_2p = pwmio.PWMOut(MOTOR_2_P, frequency=FREQUENCY)
pwm_2n = pwmio.PWMOut(MOTOR_2_N, frequency=FREQUENCY)
motor2 = motor.DCMotor(pwm_2p, pwm_2n)

# Set the motor decay modes (if unset the default will be FAST_DECAY)
motor1.decay_mode = DECAY_MODE
motor2.decay_mode = DECAY_MODE


# Turn on the Pico's LED to show the program is running
led.value = True

def button_pressed():
    return not button_a.value

# Run the motor sequence
while True:
    # Forward slow
    motor1.throttle = 0.5
    motor2.throttle = -0.5
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Stop
    motor1.throttle = 0
    motor2.throttle = 0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Forward fast
    motor1.throttle = 1.0
    motor2.throttle = -1.0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Spin freely
    motor1.throttle = None
    motor2.throttle = None
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Backwards slow
    motor1.throttle = -0.5
    motor2.throttle = 0.5
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Stop
    motor1.throttle = 0
    motor2.throttle = 0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Backwards fast
    motor1.throttle = -1.0
    motor2.throttle = 1.0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Spin freely
    motor1.throttle = None
    motor2.throttle = None
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

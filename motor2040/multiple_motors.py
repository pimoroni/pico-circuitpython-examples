# SPDX-License-Identifier: MIT

import time
import board
import pwmio
import digitalio
from adafruit_motor import motor

# Motor constants
FREQUENCY = 25000               # Chose a frequency above human hearing
DECAY_MODE = motor.SLOW_DECAY   # The decay mode affects how the motor
                                # responds, with SLOW_DECAY having improved spin
                                # threshold and speed-to-throttle linearity

# Create a digitalinout object for the user switch
user_sw = digitalio.DigitalInOut(board.USER_SW)
user_sw.direction = digitalio.Direction.INPUT
user_sw.pull = digitalio.Pull.UP

# Create the pwm objects
pwm_a_p = pwmio.PWMOut(board.MOTOR_A_P, frequency=FREQUENCY)
pwm_a_n = pwmio.PWMOut(board.MOTOR_A_N, frequency=FREQUENCY)
pwm_b_p = pwmio.PWMOut(board.MOTOR_B_P, frequency=FREQUENCY)
pwm_b_n = pwmio.PWMOut(board.MOTOR_B_N, frequency=FREQUENCY)
pwm_c_p = pwmio.PWMOut(board.MOTOR_C_P, frequency=FREQUENCY)
pwm_c_n = pwmio.PWMOut(board.MOTOR_C_N, frequency=FREQUENCY)
pwm_d_p = pwmio.PWMOut(board.MOTOR_D_P, frequency=FREQUENCY)
pwm_d_n = pwmio.PWMOut(board.MOTOR_D_N, frequency=FREQUENCY)

# Create the motor objects
mot_a = motor.DCMotor(pwm_a_p, pwm_a_n)
mot_b = motor.DCMotor(pwm_b_p, pwm_b_n)
mot_c = motor.DCMotor(pwm_c_p, pwm_c_n)
mot_d = motor.DCMotor(pwm_d_p, pwm_d_n)

# Set the motor decay modes (if unset the default will be FAST_DECAY)
mot_a.decay_mode = DECAY_MODE
mot_b.decay_mode = DECAY_MODE
mot_c.decay_mode = DECAY_MODE
mot_d.decay_mode = DECAY_MODE


def button_pressed():
    return not user_sw.value


# Run the motor sequence
while True:
    # Forward slow
    mot_a.throttle = 0.5
    mot_b.throttle = 0.5
    mot_c.throttle = 0.5
    mot_d.throttle = 0.5
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Stop
    mot_a.throttle = 0
    mot_b.throttle = 0
    mot_c.throttle = 0
    mot_d.throttle = 0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Forward fast
    mot_a.throttle = 1.0
    mot_b.throttle = 1.0
    mot_c.throttle = 1.0
    mot_d.throttle = 1.0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Spin freely
    mot_a.throttle = None
    mot_b.throttle = None
    mot_c.throttle = None
    mot_d.throttle = None
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Backwards slow
    mot_a.throttle = -0.5
    mot_b.throttle = -0.5
    mot_c.throttle = -0.5
    mot_d.throttle = -0.5
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Stop
    mot_a.throttle = 0
    mot_b.throttle = 0
    mot_c.throttle = 0
    mot_d.throttle = 0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Backwards fast
    mot_a.throttle = -1.0
    mot_b.throttle = -1.0
    mot_c.throttle = -1.0
    mot_d.throttle = -1.0
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

    # Spin freely
    mot_a.throttle = None
    mot_b.throttle = None
    mot_c.throttle = None
    mot_d.throttle = None
    time.sleep(1)
    if button_pressed():  # Exit if button is pressed
        break

# SPDX-License-Identifier: MIT

import time
import board
import math
import random
import pwmio
import digitalio
import rotaryio
from adafruit_motor import motor

# Pin constants
MOTOR_P = board.MOTOR_A_P
MOTOR_N = board.MOTOR_A_N
CHANNEL_A = board.ENCODER_A_A
CHANNEL_B = board.ENCODER_A_B

# Setting constants
FREQUENCY = 25000                   # Chose a frequency above human hearing
DECAY_MODE = motor.SLOW_DECAY       # The decay mode affects how the motor
                                    # responds, with SLOW_DECAY having improved spin
                                    # threshold and speed-to-throttle linearity
GEAR_RATIO = 50                     # The gear ratio of the motor
COUNTS_PER_REV = 12 * GEAR_RATIO    # The counts per revolution of the motor's output shaft
UPDATES = 100                       # How many times to update the motor per second
UPDATE_RATE = 1 / UPDATES
TIME_FOR_EACH_MOVE = 1              # The time to travel between each random value
UPDATES_PER_MOVE = TIME_FOR_EACH_MOVE * UPDATES
PRINT_DIVIDER = 4                   # How many of the updates should be printed (i.e. 2 would be every other update)
SPEED_SCALE = 5.4                   # The scaling to apply to the motor's speed to match its real-world speed

# Multipliers for the different printed values, so they appear nicely on the Thonny plotter
SPD_PRINT_SCALE = 20                # Driving Speed multipler

POSITION_EXTENT = 180               # How far from zero to move the motor, in degrees
INTERP_MODE = 2                     # The interpolating mode between setpoints. STEP (0), LINEAR (1), COSINE (2)


# PID values
POS_KP = 0.14                       # Position proportional (P) gain
POS_KI = 0.0                        # Position integral (I) gain
POS_KD = 0.0022                     # Position derivative (D) gain

# Create a digitalinout object for the user switch
user_sw = digitalio.DigitalInOut(board.USER_SW)
user_sw.direction = digitalio.Direction.INPUT
user_sw.pull = digitalio.Pull.UP

# Create the pwm and objects
pwm_p = pwmio.PWMOut(MOTOR_P, frequency=FREQUENCY)
pwm_n = pwmio.PWMOut(MOTOR_N, frequency=FREQUENCY)
mot = motor.DCMotor(pwm_p, pwm_n)

# Set the motor decay modes (if unset the default will be FAST_DECAY)
mot.decay_mode = DECAY_MODE

# Create the encoder object
encoder = rotaryio.IncrementalEncoder(CHANNEL_B, CHANNEL_A, divisor=1)


# A simple class for handling Proportional, Integral & Derivative (PID) control calculations
class PID:
    def __init__(self, kp, ki, kd, sample_rate):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = 0
        self._error_sum = 0
        self._last_value = 0
        self._sample_rate = sample_rate

    def calculate(self, value):
        error = self.setpoint - value
        self._error_sum += error * self._sample_rate
        rate_error = (value - self._last_value) / self._sample_rate
        self._last_value = value

        return (error * self.kp) + (self._error_sum * self.ki) - (rate_error * self.kd)


def button_pressed():
    return not user_sw.value


def to_degrees(position):
    return (position * 360.0) / COUNTS_PER_REV


# Create PID object for position control
pos_pid = PID(POS_KP, POS_KI, POS_KD, UPDATE_RATE)

update = 0
print_count = 0

# Set the initial value and create a random end value between the extents
start_value = 0.0
end_value = random.uniform(-POSITION_EXTENT, POSITION_EXTENT)

# Run until the user switch is pressed
while not button_pressed():

    # Capture the state of the encoder
    angle = to_degrees(encoder.position)

    # Calculate how far along this movement to be
    percent_along = min(update / UPDATES_PER_MOVE, 1.0)

    if INTERP_MODE == 0:
        # Move the motor instantly to the end value
        pos_pid.setpoint = end_value
    elif INTERP_MODE == 2:
        # Move the motor between values using cosine
        pos_pid.setpoint = (((-math.cos(percent_along * math.pi) + 1.0) / 2.0) * (end_value - start_value)) + start_value
    else:
        # Move the motor linearly between values
        pos_pid.setpoint = (percent_along * (end_value - start_value)) + start_value

    # Calculate the velocity to move the motor closer to the position setpoint
    vel = pos_pid.calculate(angle)

    # Set the new motor driving speed
    mot.throttle = max(min(vel / SPEED_SCALE, 1.0), -1.0)

    # Print out the current motor values and their setpoints, but only on every multiple
    if print_count == 0:
        print("Pos =", angle, end=", ")
        print("Pos SP =", pos_pid.setpoint, end=", ")
        print("Speed =", mot.throttle * SPEED_SCALE * SPD_PRINT_SCALE)

    # Increment the print count, and wrap it
    print_count = (print_count + 1) % PRINT_DIVIDER

    update += 1     # Move along in time

    # Have we reached the end of this movement?
    if update >= UPDATES_PER_MOVE:
        update = 0  # Reset the counter

        # Set the start as the last end and create a new random end value
        start_value = end_value
        end_value = random.uniform(-POSITION_EXTENT, POSITION_EXTENT)

    time.sleep(UPDATE_RATE)

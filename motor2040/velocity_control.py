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

SPEED_SCALE = 5.4                   # The scaling to apply to each motor's speed to match its real-world speed

UPDATES = 100                       # How many times to update the motor per second
UPDATE_RATE = 1 / UPDATES
TIME_FOR_EACH_MOVE = 1              # The time to travel between each random value
UPDATES_PER_MOVE = TIME_FOR_EACH_MOVE * UPDATES
PRINT_DIVIDER = 4                   # How many of the updates should be printed (i.e. 2 would be every other update)

# Multipliers for the different printed values, so they appear nicely on the Thonny plotter
ACC_PRINT_SCALE = 0.05              # Acceleration multiplier

VELOCITY_EXTENT = 3                 # How far from zero to drive the motor at, in revolutions per second
INTERP_MODE = 2                     # The interpolating mode between setpoints. STEP (0), LINEAR (1), COSINE (2)

# PID values
VEL_KP = 30.0                       # Velocity proportional (P) gain
VEL_KI = 0.0                        # Velocity integral (I) gain
VEL_KD = 0.4                        # Velocity derivative (D) gain

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


def to_revs(position):
    return position / COUNTS_PER_REV


# Create PID object for velocity control
vel_pid = PID(VEL_KP, VEL_KI, VEL_KD, UPDATE_RATE)

update = 0
print_count = 0

# Initialise the motor
mot.throttle = 0.0

# Set the initial value and create a random end value between the extents
start_value = 0.0
end_value = random.uniform(-VELOCITY_EXTENT, VELOCITY_EXTENT)

revs = 0.0
last_revs = 0.0

# Run until the user switch is pressed
while not button_pressed():

    # Capture the state of the encoder
    last_revs = revs
    revs = to_revs(encoder.position)

    # Calculate how far along this movement to be
    percent_along = min(update / UPDATES_PER_MOVE, 1.0)

    if INTERP_MODE == 0:
        # Move the motor instantly to the end value
        vel_pid.setpoint = end_value
    elif INTERP_MODE == 2:
        # Move the motor between values using cosine
        vel_pid.setpoint = (((-math.cos(percent_along * math.pi) + 1.0) / 2.0) * (end_value - start_value)) + start_value
    else:
        # Move the motor linearly between values
        vel_pid.setpoint = (percent_along * (end_value - start_value)) + start_value

    # Calculate the acceleration to apply to the motor to move it closer to the velocity setpoint
    vel = (revs - last_revs) / UPDATE_RATE
    accel = vel_pid.calculate(vel)

    # Set the new motor driving speed
    mot.throttle = max(min(mot.throttle + ((accel * UPDATE_RATE) / SPEED_SCALE), 1.0), -1.0)

    # Print out the current motor values and their setpoints, but only on every multiple
    if print_count == 0:
        print("Vel =", vel, end=", ")
        print("Vel SP =", vel_pid.setpoint, end=", ")
        print("Accel =", accel * ACC_PRINT_SCALE, end=", ")
        print("Speed =", mot.throttle * SPEED_SCALE)

    # Increment the print count, and wrap it
    print_count = (print_count + 1) % PRINT_DIVIDER

    update += 1     # Move along in time

    # Have we reached the end of this movement?
    if update >= UPDATES_PER_MOVE:
        update = 0  # Reset the counter

        # Set the start as the last end and create a new random end value
        start_value = end_value
        end_value = random.uniform(-VELOCITY_EXTENT, VELOCITY_EXTENT)

    time.sleep(UPDATE_RATE)

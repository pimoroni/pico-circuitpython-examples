# SPDX-License-Identifier: MIT

import time
import board
import pwmio
import digitalio
import rotaryio
from adafruit_motor import motor

# Wheel friendly names
FL = 2
FR = 3
RL = 1
RR = 0

# Setting constants
FREQUENCY = 25000                   # Chose a frequency above human hearing
DECAY_MODE = motor.SLOW_DECAY       # The decay mode affects how the motor
                                    # responds, with SLOW_DECAY having improved spin
                                    # threshold and speed-to-throttle linearity
GEAR_RATIO = 50                     # The gear ratio of the motor
COUNTS_PER_REV = 12 * GEAR_RATIO    # The counts per revolution of the motor's output shaft

SPEED_SCALE = 5.4                       # The scaling to apply to each motor's speed to match its real-world speed

UPDATES = 100                       # How many times to update the motor per second
UPDATE_RATE = 1 / UPDATES
TIME_FOR_EACH_MOVE = 1              # The time to travel between each random value
UPDATES_PER_MOVE = TIME_FOR_EACH_MOVE * UPDATES
PRINT_DIVIDER = 4                   # How many of the updates should be printed (i.e. 2 would be every other update)

DRIVING_SPEED = 1.0                 # The speed to drive the wheels at, from 0.0 to SPEED_SCALE

# PID values
VEL_KP = 30.0                       # Velocity proportional (P) gain
VEL_KI = 0.0                        # Velocity integral (I) gain
VEL_KD = 0.4                        # Velocity derivative (D) gain

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
mot_b = motor.DCMotor(pwm_b_n, pwm_b_p)     # Reversed direction
mot_c = motor.DCMotor(pwm_c_n, pwm_c_p)     # Reversed direction
mot_d = motor.DCMotor(pwm_d_p, pwm_d_n)
motors = [mot_a, mot_b, mot_c, mot_d]

# Set the motor decay modes (if unset the default will be FAST_DECAY)
mot_a.decay_mode = DECAY_MODE
mot_b.decay_mode = DECAY_MODE
mot_c.decay_mode = DECAY_MODE
mot_d.decay_mode = DECAY_MODE

# Create the encoder objects
enc_a = rotaryio.IncrementalEncoder(board.ENCODER_A_B, board.ENCODER_A_A, divisor=1)
enc_b = rotaryio.IncrementalEncoder(board.ENCODER_B_A, board.ENCODER_B_B, divisor=1)     # Reversed direction
enc_c = rotaryio.IncrementalEncoder(board.ENCODER_C_A, board.ENCODER_C_B, divisor=1)     # Reversed direction
enc_d = rotaryio.IncrementalEncoder(board.ENCODER_D_B, board.ENCODER_D_A, divisor=1)
encoders = [enc_a, enc_b, enc_c, enc_d]
ENCODER_NAMES = ["RR", "RL", "FL", "FR"]


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


# Helper functions for driving in common directions
def drive_forward(speed):
    vel_pids[FL].setpoint = speed
    vel_pids[FR].setpoint = speed
    vel_pids[RL].setpoint = speed
    vel_pids[RR].setpoint = speed


def turn_right(speed):
    vel_pids[FL].setpoint = speed
    vel_pids[FR].setpoint = -speed
    vel_pids[RL].setpoint = speed
    vel_pids[RR].setpoint = -speed


def strafe_right(speed):
    vel_pids[FL].setpoint = speed
    vel_pids[FR].setpoint = -speed
    vel_pids[RL].setpoint = -speed
    vel_pids[RR].setpoint = speed


def stop():
    vel_pids[FL].setpoint = 0
    vel_pids[FR].setpoint = 0
    vel_pids[RL].setpoint = 0
    vel_pids[RR].setpoint = 0


# Create PID objects for velocity control
vel_pids = [PID(VEL_KP, VEL_KI, VEL_KD, UPDATE_RATE) for i in range(board.NUM_MOTORS)]

update = 0
print_count = 0
sequence = 0

# Initialise the motors
for i in range(board.NUM_MOTORS):
    motors[i].throttle = 0.0

revs = [0.0] * board.NUM_MOTORS
last_revs = [0.0] * board.NUM_MOTORS

# Run until the user switch is pressed
while not button_pressed():

    for i in range(board.NUM_MOTORS):
        # Capture the state of the encoder
        last_revs[i] = revs[i]
        revs[i] = to_revs(encoders[i].position)

    for i in range(board.NUM_MOTORS):
        vel = (revs[i] - last_revs[i]) / UPDATE_RATE

        # Calculate the acceleration to apply to the motor to move it closer to the velocity setpoint
        accel = vel_pids[i].calculate(vel)

        # Accelerate or decelerate the motor
        motors[i].throttle = max(min(motors[i].throttle + ((accel * UPDATE_RATE) / SPEED_SCALE), 1.0), -1.0)

    # Print out the current motor values, but only on every multiple
    if print_count == 0:
        for i in range(board.NUM_MOTORS):
            print(ENCODER_NAMES[i], "=", revs[i], end=", ")
        print()

    # Increment the print count, and wrap it
    print_count = (print_count + 1) % PRINT_DIVIDER

    update += 1     # Move along in time

    # Have we reached the end of this movement?
    if update >= UPDATES_PER_MOVE:
        update = 0  # Reset the counter

        # Move on to the next part of the sequence
        sequence += 1

        # Loop the sequence back around
        if sequence >= 7:
            sequence = 0

    # Set the motor speeds, based on the sequence
    if sequence == 0:
        drive_forward(DRIVING_SPEED)
    elif sequence == 1:
        drive_forward(-DRIVING_SPEED)
    elif sequence == 2:
        turn_right(DRIVING_SPEED)
    elif sequence == 3:
        turn_right(-DRIVING_SPEED)
    elif sequence == 4:
        strafe_right(DRIVING_SPEED)
    elif sequence == 5:
        strafe_right(-DRIVING_SPEED)
    elif sequence == 6:
        stop()

    time.sleep(UPDATE_RATE)

# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Analog In example"""
import time
import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn

addr0_pin = DigitalInOut(board.ADC_ADDR_0)
addr0_pin.direction = Direction.OUTPUT

addr1_pin = DigitalInOut(board.ADC_ADDR_1)
addr1_pin.direction = Direction.OUTPUT

addr2_pin = DigitalInOut(board.ADC_ADDR_2)
addr2_pin.direction = Direction.OUTPUT

analog_in = AnalogIn(board.SHARED_ADC)


def get_voltage(pin):
    return (pin.value * 3.3) / 65536


def select(address):
    addr0_pin.value = address & 0b001
    addr1_pin.value = address & 0b010
    addr2_pin.value = address & 0b100


VOLTAGE_GAIN = 13.9 / 3.9
CURRENT_GAIN = 1 / 0.47
CURRENT_OFFSET = -0.005

while True:
    # Read each sensor in turn and print its voltage
    for i in range(board.NUM_SENSORS):
        select(i + board.SENSOR_1_ADDR)
        print("S", i + 1, " = ", round(get_voltage(analog_in), 3), sep="", end=", ")

    # Read the voltage sense and print the value
    select(board.VOLTAGE_SENSE_ADDR)
    voltage = get_voltage(analog_in) * VOLTAGE_GAIN
    print("Voltage =", round(voltage, 4), end=", ")

    # Read the current sense and print the value
    for i in range(board.NUM_MOTORS):
        select(i + board.CURRENT_SENSE_A_ADDR)
        current = (get_voltage(analog_in) + CURRENT_OFFSET) * CURRENT_GAIN
        print("C", i + 1, " = ", round(current, 4), sep="", end=", ")

    print()

    time.sleep(0.5)

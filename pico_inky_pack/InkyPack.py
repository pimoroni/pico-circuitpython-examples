# -------------------------------------------------------------------------
# Class InkyPack for Pimoroni's Inky-Pack e-Paper.
#
# The Inky-Pack uses an UC8151-chip, but the standard UC8151D-class from
# https://github.com/adafruit/Adafruit_CircuitPython_UC8151D
# does not support this display.
#
# The start-sequence and stop-sequence were copied from the board.c
# definition-file of the Badger2040 which uses the same display.
#
# Author: Bernhard Bablok
# License: The MIT License (MIT)
#
# -------------------------------------------------------------------------

import board
import displayio

_START_SEQUENCE = (
    b"\x01\x05\x03\x00\x2b\x2b\x2b"          # power setting
    b"\x04\x80\xc8"                          # power on and wait 200 ms
    b"\x06\x03\x17\x17\x17"
    b"\x00\x01\xbf"
    b"\x03\x01\x00"
    b"\x41\x01\x00"
    b"\x60\x01\x22" # tcon setting
    b"\x50\x01\x4c" # vcom and data interval
    b"\x30\x01\x3a" # PLL set to 100 Hz
    # Look up tables for voltage sequence for pixel transition
    # Common voltage
    b"\x20\x2c"
    b"\x00\x16\x16\x0d\x00\x01"
    b"\x00\x23\x23\x00\x00\x02"
    b"\x00\x16\x16\x0d\x00\x01"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00"
    # White to white
    b"\x21\x2a"
    b"\x54\x16\x16\x0d\x00\x01"
    b"\x60\x23\x23\x00\x00\x02"
    b"\xa8\x16\x16\x0d\x00\x01"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    # Black to white
    b"\x22\x2a"
    b"\x54\x16\x16\x0d\x00\x01"
    b"\x60\x23\x23\x00\x00\x02"
    b"\xa8\x16\x16\x0d\x00\x01"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    # White to black
    b"\x23\x2a"
    b"\xa8\x16\x16\x0d\x00\x01"
    b"\x60\x23\x23\x00\x00\x02"
    b"\x54\x16\x16\x0d\x00\x01"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    # Black to black
    b"\x24\x2a"
    b"\xa8\x16\x16\x0d\x00\x01"
    b"\x60\x23\x23\x00\x00\x02"
    b"\x54\x16\x16\x0d\x00\x01"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00"
)

_STOP_SEQUENCE = b"\x02\x00"  #Power off

class InkyPack(displayio.EPaperDisplay):
  r"""InkyPack UC8151 driver

  :param bus: The data bus the display is on
  :param \**kwargs:
    See below

    :Keyword Arguments:
      * *width* (``int``) --
      Display width
      * *height* (``int``) --
      Display height
      * *rotation* (``int``) --
          Display rotation
  """

  def __init__(self, bus: displayio.FourWire, **kwargs) -> None:
    super().__init__(
      bus,
      _START_SEQUENCE,
      _STOP_SEQUENCE,
      **kwargs,
      width=296,
      height=128,
      ram_width=160,
      ram_height=296,
      rotation=270,
      busy_state=False,
      write_black_ram_command=0x13,
      write_color_ram_command=0x10,
      refresh_display_command=0x12,
      seconds_per_frame=2,
      black_bits_inverted=True,
      refresh_time=1.0,
    )

# -------------------------------------------------------------------------
# Testprogram for Pimoroni's Inky-Pack e-Paper.
#
# This program is an adaption of Adafruit's uc8151d_simpletest.py from
# https://github.com/adafruit/Adafruit_CircuitPython_UC8151D
#
# Author: Bernhard Bablok
# License: MIT
#
# -------------------------------------------------------------------------

# pylint: disable=no-member

import time
import board
import busio
import displayio
import InkyPack

displayio.release_displays()

# pinout for Pimoroni Inky Pack

SCK_PIN  = board.GP18
MOSI_PIN = board.GP19
MISO_PIN = board.GP16
CS_PIN   = board.GP17
RST_PIN  = board.GP21
DC_PIN   = board.GP20
BUSY_PIN = board.GP26

spi = busio.SPI(SCK_PIN,MOSI=MOSI_PIN,MISO=MISO_PIN)
display_bus = displayio.FourWire(
  spi, command=DC_PIN, chip_select=CS_PIN, reset=RST_PIN, baudrate=1000000
)

display = InkyPack.InkyPack(display_bus,busy_pin=BUSY_PIN)

g = displayio.Group()

with open("/display-ruler.bmp", "rb") as f:
  pic = displayio.OnDiskBitmap(f)
  t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
  g.append(t)

  display.show(g)
  display.refresh()
  time.sleep(120)

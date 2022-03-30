import time
import board
import terminalio
import displayio
import digitalio
import vectorio
from adafruit_display_text import label

"""
An extension to the DisplayIO example that includes the activity LED
as well as puts the board to sleep once the screen has been updated.

To wake your badger when on battery, hold down any of the
front buttons until the activity light stops flashing.
"""

display = board.DISPLAY
enable = board.ENABLE_DIO

# Set up and turn on the activity LED
act = digitalio.DigitalInOut(board.USER_LED)
act.direction = digitalio.Direction.OUTPUT
act.value = True

# Set text, font, and color
title = "HELLO WORLD"
subtitle = "From CircuitPython"
font = terminalio.FONT
color = 0x000000

# Set the palette for the background color
palette = displayio.Palette(1)
palette[0] = 0xFFFFFF

# Add a background rectangle
rectangle = vectorio.Rectangle(pixel_shader=palette, width=display.width + 1, height=display.height, x=0, y=0)

# Create the title and subtitle labels
title_label = label.Label(font, text=title, color=color, scale=4)
subtitle_label = label.Label(font, text=subtitle, color=color, scale=2)

# Set the label locations
title_label.x = 20
title_label.y = 45

subtitle_label.x = 40
subtitle_label.y = 90

# Create the display group and append objects to it
group = displayio.Group()
group.append(rectangle)
group.append(title_label)
group.append(subtitle_label)

# Show the group and refresh the screen to see the result
display.show(group)
display.refresh()

# Wait a few seconds for the screen to refresh
time.sleep(3)

# Turn the board off
enable.value = False

# Loop forever so you can enjoy your message when on USB power
# When on battery this will never be reached, as indicated
# by the activity LED turning off rather than flashing
while True:
    act.value = False
    time.sleep(0.25)
    act.value = True
    time.sleep(0.25)

import time
import board
import digitalio
from analogio import AnalogIn
import adafruit_rgbled
import busio
import neopixel
import adafruit_dotstar as dotstar
import math

# Press "B" to speed up the LED cycling effect.
# Press "A" to slow it down again.
# Press "Boot" to reset the speed back to default.


# Set how many LEDs you have
NUM_LEDS = 30

# The speed that the LEDs will start cycling at
DEFAULT_SPEED = 10

# How many times the LEDs will be updated per second
UPDATES = 60

# How bright the LEDs will be (between 0.0 and 1.0)
BRIGHTNESS = 0.5


# Pick *one* LED type by uncommenting the relevant line below:

# APA102 / DotStar™ LEDs
# led_strip = dotstar.DotStar(board.CLK, board.DATA, NUM_LEDS, brightness=BRIGHTNESS)

# WS2812 / NeoPixel™ LEDs
led_strip = neopixel.NeoPixel(board.DATA, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

user_sw = digitalio.DigitalInOut(board.USER_SW)
user_sw.direction = digitalio.Direction.INPUT
user_sw.pull = digitalio.Pull.UP

sw_a = digitalio.DigitalInOut(board.SW_A)
sw_a.direction = digitalio.Direction.INPUT
sw_a.pull = digitalio.Pull.UP

sw_b = digitalio.DigitalInOut(board.SW_B)
sw_b.direction = digitalio.Direction.INPUT
sw_b.pull = digitalio.Pull.UP

led = adafruit_rgbled.RGBLED(board.LED_R, board.LED_G, board.LED_B, invert_pwm = True)

sense = AnalogIn(board.CURRENT_SENSE)

# Constants used for current conversion
ADC_GAIN = 50
SHUNT_RESISTOR = 0.015 # Yes, this is 0.015 Ohm

def get_voltage(pin):
    return (pin.value * 3.3) / 65536
    
def get_current(pin):
    return get_voltage(pin) / (ADC_GAIN * SHUNT_RESISTOR)

def hsv_to_rgb(h, s, v):
	# All inputs are from 0.0 to 1.0
    i = math.floor(h * 6.0)
    f = h * 6.0 - i
    v *= 255.0
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)

    zone = int(i) % 6
    if zone == 0:
        return (v, t, p)
    if zone == 1:
	    return (q, v, p)
    if zone == 2:
        return (p, v, t)
    if zone == 3:
	    return (p, q, v)
    if zone == 4:
	    return (t, p, v)
    if zone == 5:
		return (v, p, q)
    return (0, 0, 0)

def button_read(button):
	return not button.value

speed = DEFAULT_SPEED
offset = 0.0

count = 0
# Make rainbows
while True:
    sw = not user_sw.value
    a = not sw_a.value
    b = not sw_b.value
	
    if sw:
		speed = DEFAULT_SPEED
    else:
        if a:
            speed -= 1
        if b:
            speed += 1
			
	speed = min(255, max(1, speed))
	
	offset += float(speed) / 2000.0

    for i in range(NUM_LEDS):
        hue = float(i) / NUM_LEDS
        led_strip[i] = hsv_to_rgb(hue + offset, 1.0, 1.0)
	led_strip.show()
	
    led.color = (speed, 0, 255 - speed)

    count += 1
    if count >= UPDATES:
        # Display the current value once every second
        print("Current =", get_current(sense), "A")
        count = 0

    time.sleep(1.0 / UPDATES)

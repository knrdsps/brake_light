import board
import time
import neopixel
import digitalio as dio
from supervisor import ticks_ms

RED = (0xFF, 0x00, 0x00)
GREEN = (0x00, 0xFF, 0x00)
AMBER = (255, 42, 0)
OFF = (0x00, 0x00, 0x00)
pixel_pin = board.D4
num_pixels = 40
brk = dio.DigitalInOut(board.D0)
brk.direction = dio.Direction.INPUT
brk.pull = dio.Pull.UP

#v2.2 kinda just copied James' code from above :)
haz = dio.DigitalInOut(board.D1)
haz.direction = dio.Direction.INPUT
haz.pull = dio.Pull.UP

rookie = dio.DigitalInOut(board.D2)
rookie.direction = dio.Direction.INPUT
rookie.pull = dio.Pull.UP

rain = dio.DigitalInOut(board.D3)
rain.direction = dio.Direction.INPUT
rain.pull = dio.Pull.UP

#v2.0 easier to change brightness for testing:
#v2.2!THIS IS SET TO FULL BY DEFAULT!
test_brightness = 0.05
full_brightness = 1

# auto_write will automatically call pixels.show() whenever the pixels are updated.
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=full_brightness, auto_write=True)
start = ticks_ms()

period1 = 100
period2 = 150

def LightStatus(dt):
    if not brk.value:
        before = RED
        after = RED
    else:
        if not haz.value:
            before = AMBER
            if not rookie.value:
                after = GREEN
            else:
                after = OFF
        else:
            if not rookie.value:
                before = GREEN
                if not rain.value:
                    state = dt % ((period1 + period2)*2)
                    if state < period1:
                       return RED
                    elif state < period2+period1:
                        return OFF
                    elif state < period1*2+period2:
                        return GREEN
                    else:
                        return OFF
                else:
                    after = OFF
            else:
                after = OFF
                if not rain.value:
                    before = RED
                else:
                    before = OFF
    return before if dt % (period1 + period2) < period1 else after

while True:
    pixels.fill(LightStatus((ticks_ms()-start)))

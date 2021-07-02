from neopixel import NeoPixel
from machine import Pin
from .util import sub_tuple, add_tuple, multiply_tuple
import time


class LEDDriver:

    LED_PIN = 4
    MAX_HUE = 150

    def __init__(self, leds, meters) -> None:
        self.len_leds = leds * meters
        self.pixels = NeoPixel(Pin(self.LED_PIN, Pin.OUT), self.len_leds)

    def write(self):
        self.pixels.write()

    def set_all(self, rgb):
        for counter in range(self.len_leds):
            self.pixels[counter] = rgb

    def dimm_desc(self, factor=5, steps=5):
        for _ in range(steps):
            self.dimm_all(factor=factor, ascending=False)
            self.write()

    def dimm_asc(self, factor=5, steps=5):
        for _ in range(steps):
            self.dimm_all(factor=factor, ascending=True)
            self.write()

    def dimm_pixel(self, rgb, factor, ascending):
        factors = multiply_tuple(
            tuple([1 if color > 0 else 0 for color in rgb]), (factor, factor, factor)
        )
        if ascending:
            if any([color >= self.MAX_HUE for color in rgb]):
                return tuple(
                    [color if color < self.MAX_HUE else self.MAX_HUE for color in rgb]
                )
            return add_tuple(rgb, factors)
        else:
            if all([color < 0 for color in rgb]):
                return tuple([color if color > 0 else 0 for color in rgb])
            return sub_tuple(rgb, factors)

    def dimm_all(self, factor=5, ascending=False):
        for counter in range(self.len_leds):
            self.pixels[counter] = self.dimm_pixel(
                self.pixels[counter], factor=factor, ascending=ascending
            )

    def reset(self):
        self.black()
        self.write()

    # def moving_snake(self, length=10, rgb=(40,200,80)):
    #     for counter in range(length):
    #         self.pixels[counter]
    #     for i in range(length,)
    def black(self):
        self.set_all((0, 0, 0))

    def red(self):
        self.set_all((self.MAX_HUE, 0, 0))

    def green(self):
        self.set_all((0, self.MAX_HUE, 0))

    def purple(self):
        self.set_all((self.MAX_HUE, 0, self.MAX_HUE))

    def blue(self):
        self.set_all((0, 0, self.MAX_HUE))

    def loop(self, count):
        self.set_all((25, 0, 0))
        self.write()
        self.dimm_asc(factor=5, steps=35)
        self.dimm_desc(factor=5, steps=35)
        self.set_all((0, 25, 0))
        self.write()
        self.dimm_asc(factor=5, steps=35)
        self.dimm_desc(factor=5, steps=35)
        self.set_all((0, 0, 25))
        self.write()
        self.dimm_asc(factor=5, steps=35)
        self.dimm_desc(factor=5, steps=35)

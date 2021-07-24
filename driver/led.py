import gc

import uasyncio
from apiserver.objects.animation import Animation
from apiserver.objects.rgb import RGB
from machine import Pin
from neopixel import NeoPixel

from .util import add_tuple, multiply_tuple, sub_tuple


class LEDDriver:

    LED_PIN = 4
    BLACK = RGB(0, 0, 0)
    MAX_HUE = 255

    def __init__(self, leds, meters) -> None:
        self.len_leds = leds * meters
        self.pixels = NeoPixel(Pin(self.LED_PIN, Pin.OUT), self.len_leds)
        self.position = 0
        self.color = self.BLACK
        self.animation: Animation = Animation(animation="normal")

    async def write(self):
        await self.pixels.write()
        print("Pixels")

    async def start(self):
        count = 0
        while True:
            count += 1
            if count >= 60:
                count = 0
            await self.loop(count)
            gc.collect()
            await uasyncio.sleep_ms(10)

    def set(self, rgb, unit):
        self.pixels[unit] = rgb

    def set_animation(self, animation: Animation):
        self.animation = animation

    def set_all(self, rgb):
        for counter in range(self.len_leds):
            self.set(rgb, counter)

    def dimm_desc(self, factor=5, steps=5):
        for _ in range(steps):
            self.dimm_all(factor=factor, ascending=False)
            self.write()

    def moving_snake(self, length=10):
        if self.position - length - 1 == self.len_leds and self.position != 0:
            self.position = 0
        elif self.position <= length:
            for i in range(0, self.position):
                self.pixels[i] = self.color.as_vector()
        elif self.position > length and self.position <= self.len_leds:
            for i in range(self.position - length, self.position):
                self.pixels[i] = self.color.as_vector()
            for i in range(0, self.position - length):
                self.pixels[i] = self.BLACK.as_vector()
        elif self.position > self.len_leds:
            for i in range(self.position - length, self.len_leds):
                self.pixels[i] = self.color.as_vector()
            for i in range(0, self.position - length):
                self.pixels[i] = self.BLACK.as_vector()
        self.position += 1

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
        self.set_all(self.BLACK.as_vector())
        self.write()

    async def loop(self, count):
        if self.animation == Animation("snake"):
            self.moving_snake()
        elif self.animation == Animation("breath"):
            print("Not Implemented the breath animation.")
            pass
        elif self.animation == Animation("off"):
            self.reset()
            return
        else:
            self.set_all(self.color.as_vector())
        self.write()
        print("Hello from LED Driver :: {}".format(count))

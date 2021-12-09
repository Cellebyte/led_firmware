from collections import OrderedDict
import driver.color_store
import driver.led
import driver.store
from objects.animation import Animation
from objects.rgb import COLORS

import animations.normal


class Snake(animations.normal.Normal):
    ANIMATION: Animation = Animation("snake")

    def __init__(
        self,
        store: driver.store.Store,
        color_store: driver.color_store.ColorStore,
        leds: driver.led.LEDDriver,
    ):
        super().__init__(store, color_store, leds)
        self.position = 0
        self.end_position = 0

    @property
    def steps(self) -> int:
        data = self.store.load(self.get_key("steps"), default=1)
        assert isinstance(data, int)
        return data

    @steps.setter
    def steps(self, value: int):
        assert isinstance(value, int)
        self.store.save(self.get_key("steps"), value)

    @property
    def length(self) -> int:
        data = self.store.load(self.get_key("length"), default=30)
        assert isinstance(data, int)
        return data

    @length.setter
    def length(self, value: int):
        assert isinstance(value, int)
        self.store.save(self.get_key("length"), value)

    def update(self, data: dict):
        if "length" in data.keys() and int(data["length"]) != self.length:
            self.found_key = True
            self.length = int(data["length"])
        if "steps" in data.keys() and int(data["steps"]) != self.steps:
            self.found_key = True
            self.steps = int(data["steps"])
        super().update(data)
        return self

    def as_dict(self) -> dict:
        return OrderedDict(
            [("length", self.length), ("steps", self.steps)]
            + [(key, value) for key, value in super().as_dict().items()]
        )

    def loop(self):
        self.leds.reset()
        if self.position <= self.length:
            self.leds.set(self.color.normalize(), self.position)
        elif self.position > self.length and self.position <= self.leds.len_leds:
            self.end_position = 0
            self.leds.set(COLORS.BLACK, self.position - self.length)
            self.leds.set(self.color.normalize(), self.position)
        elif self.position > self.leds.len_leds:
            self.end_position = self.position
            self.position = -1
        if self.end_position > self.leds.len_leds:
            self.leds.set(COLORS.BLACK, self.end_position - self.length)
            self.end_position += self.steps
        self.position += self.steps

    # Rotate <num_of_pixels> pixels to the left
    def rotate_left(self, num_of_pixels):
        if num_of_pixels is None:
            num_of_pixels = 1
        self.pixels = self.pixels[num_of_pixels:] + self.pixels[:num_of_pixels]

    # Rotate <num_of_pixels> pixels to the right
    def rotate_right(self, num_of_pixels):
        if num_of_pixels is None:
            num_of_pixels = 1
        num_of_pixels = -1 * num_of_pixels
        self.pixels = self.pixels[num_of_pixels:] + self.pixels[:num_of_pixels]

from collections import OrderedDict

import driver.colour_palettes
import driver.led
import driver.store
from objects.animation import Animation
from objects.direction import Direction
from objects.rgb import COLOURS

import animations.normal


class Snake(animations.normal.Normal):
    ANIMATION: Animation = Animation("snake")
    _colour_selectors_max_len = 16
    direction = Direction("up")

    def __init__(
        self,
        store: driver.store.Store,
        leds: driver.led.LEDDriver,
        colour_palettes: driver.colour_palettes.ColourPalettes,
    ):
        super().__init__(store, leds, colour_palettes)
        self.position = 0
        self.end_position = self.leds.len_leds

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
        return super().update(data)

    def as_dict(self) -> dict:
        return OrderedDict(
            [
                ("length", self.length),
                ("steps", self.steps),
            ]
            + [(key, value) for key, value in super().as_dict().items()]
        )

    def loop(self):
        if self.direction.value == "up":
            if self.change_colour and self.position == 0:
                self._colour_selector_index = self._colour_selector_index + 1
            if not self._colour_selector_index < len(self.colour_selectors):
                self._colour_selector_index = 0
                return
            if self.position <= self.length:
                self.leds.set(self.colour.normalize(), self.position)
            elif self.position > self.length and self.position < self.leds.len_leds:
                self.end_position = 0
                self.leds.set(COLOURS.BLACK, self.position - self.length)
                self.leds.set(self.colour.normalize(), self.position)
            elif self.position >= self.leds.len_leds:
                self.end_position = self.position - self.length
                self.position = -1
            if self.end_position < self.leds.len_leds:
                self.leds.set(COLOURS.BLACK, self.end_position)
                self.end_position += self.steps
            self.position += self.steps
        elif self.direction.value == "down":
            raise NotImplementedError(
                "This direction {} is not implemented for Snake".format(self.direction)
            )

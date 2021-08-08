import driver.color_store
import driver.led
import driver.store
from objects.animation import Animation
from objects.constants import ANIMATION_SNAKE, LENGTH, STEPS
from objects.rgb import BLACK

import animations.normal


class Snake(animations.normal.Normal):
    ANIMATION = Animation(ANIMATION_SNAKE)

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
        return self.store.load(self.get_key(STEPS), default=1)

    @steps.setter
    def steps(self, value: int):
        assert isinstance(value, int)
        self.store.save(self.get_key(STEPS), value)

    @property
    def length(self) -> int:
        return self.store.load(self.get_key(LENGTH), default=30)

    @length.setter
    def length(self, value: int):
        assert isinstance(value, int)
        self.store.save(self.get_key(LENGTH), value)

    def update(self, data: dict):
        if LENGTH in data.keys() and int(data[LENGTH]) != self.length:
            self.found_key = True
            self.length = int(data[LENGTH])
        if STEPS in data.keys() and int(data[STEPS]) != self.steps:
            self.found_key = True
            self.steps = int(data[STEPS])
        super().update(data)
        return self

    def as_dict(self) -> dict:
        return {
            LENGTH: self.length,
            STEPS: self.steps,
        } | super().as_dict()

    def loop(self):
        self.leds.reset()
        if self.position <= self.length:
            self.leds.set(self.color.normalize(), self.position)
        elif self.position > self.length and self.position <= self.leds.len_leds:
            self.end_position = 0
            self.leds.set(BLACK, self.position - self.length)
            self.leds.set(self.color.normalize(), self.position)
        elif self.position > self.leds.len_leds:
            self.end_position = self.position
            self.position = -1
        if self.end_position > self.leds.len_leds:
            self.leds.set(BLACK, self.end_position - self.length)
            self.end_position += self.steps
        self.position += self.steps

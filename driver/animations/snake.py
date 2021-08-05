from driver.constants import PUT_NOT_USEFUL
import driver.led
import driver.store
from apiserver.objects.animation import Animation
from driver.animations.base import BaseAnimation
from apiserver.objects.rgb import PURPLE, RGB


class Snake(BaseAnimation):
    ANIMATION = Animation("snake")

    def __init__(self, store: driver.store.Store, leds: driver.led.LEDDriver):
        self.position = 0
        self.end_position = 0
        self.found_key = False
        super().__init__(store, leds)

    @property
    def color(self) -> RGB:
        return RGB(
            **self.store.load(
                "{}.color".format(self.ANIMATION.value), default=PURPLE.as_dict()
            )
        )

    @color.setter
    def color(self, value: RGB):
        assert isinstance(value, RGB)
        self.store.save("{}.color".format(self.ANIMATION.value), value.as_dict())

    @property
    def steps(self) -> int:
        return self.store.load("{}.steps".format(self.ANIMATION.value), default=1)

    @steps.setter
    def steps(self, value: int):
        assert isinstance(value, int)
        self.store.save("{}.steps".format(self.ANIMATION.value), value)

    @property
    def length(self) -> int:
        return self.store.load("{}.length".format(self.ANIMATION.value), default=30)

    @length.setter
    def length(self, value: int):
        assert isinstance(value, int)
        self.store.save("{}.length".format(self.ANIMATION.value), value)

    def update(self, data: dict):
        if "color" in data.keys() and RGB(**data["color"]) != self.color:
            self.found_key = True
            self.color = RGB(**data["color"])
        if "length" in data.keys() and int(data["length"]) != self.length:
            self.found_key = True
            self.length = int(data["length"])
        if "steps" in data.keys() and int(data["steps"]) != self.steps:
            self.found_key = True
            self.steps = int(data["steps"])
        if not self.found_key:
            raise ValueError(PUT_NOT_USEFUL)
        return self

    def as_dict(self) -> dict:
        return {
            "color": self.color.as_dict(),
            "length": self.length,
            "steps": self.steps,
        }

    def loop(self):
        self.leds.reset()
        if self.position <= self.length:
            for i in range(0, self.position):
                self.leds.set(self.color, i)
        elif self.position > self.length and self.position <= self.leds.len_leds:
            self.end_position = 0
            for i in range(self.position - self.length, self.position):
                self.leds.set(self.color, i)
        elif self.position > self.leds.len_leds:
            self.end_position = self.position
            self.position = -1
        if self.end_position > self.leds.len_leds:
            for i in range(self.end_position - self.length, self.leds.len_leds):
                self.leds.set(self.color, i)
            self.end_position += self.steps
        self.position += self.steps

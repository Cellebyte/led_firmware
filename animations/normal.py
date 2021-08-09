import driver.color_store
import driver.led
import driver.store
from errors import PUT_NOT_USEFUL
from objects.animation import Animation
from objects.rgb import BLACK

import animations.base


class Normal(animations.base.BaseAnimation):
    ANIMATION: Animation = Animation("normal")

    def __init__(
        self,
        store: driver.store.Store,
        color_store: driver.color_store.ColorStore,
        leds: driver.led.LEDDriver,
    ):
        super().__init__(store, leds)
        self.color_store: driver.color_store.ColorStore = color_store
        self.found_key: bool = False

    @property
    def color(self):
        color = self.color_store[self.color_selector]
        if color is None:
            return BLACK
        return color

    @property
    def color_selector(self) -> int:
        return self.store.load(self.get_key("color_selector"), default=1)

    @color_selector.setter
    def color_selector(self, value: int):
        assert self.color_store.validate_key(value)
        self.store.save(self.get_key("color_selector"), value)

    def update(self, data: dict):
        if (
            "color_selector" in data.keys()
            and int(data["color_selector"]) != self.color_selector
        ):
            self.found_key = True
            self.color_selector = int(data["color_selector"])
        if not self.found_key:
            self.found_key = False
            raise ValueError(PUT_NOT_USEFUL)

        return self

    def as_dict(self):
        return {"color_selector": self.color_selector, "current_color": self.color}

    def get_key(self, key):
        return "{}.{}".format(self.ANIMATION.value, key)

    def loop(self):
        self.leds.set_all(self.color.normalize())

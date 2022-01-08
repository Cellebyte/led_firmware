from collections import OrderedDict
from typing import Optional

from errors import VALUE_NOT_OF_TYPE
from objects.animation import Animation
from objects.direction import Direction

import animations.normal


class Breath(animations.normal.Normal):
    ANIMATION: Animation = Animation("breath")
    _value = None
    _colour_selectors_max_len = 10
    _direction = Direction("up")

    @property
    def value(self) -> Optional[float]:
        return self._value

    @value.setter
    def value(self, value: Optional[float]):
        if value is None:
            self._value = None
            return
        elif not isinstance(value, float):
            raise ValueError(
                VALUE_NOT_OF_TYPE(
                    self.__class__.__name__, "value", value, allowed_type=float
                )
            )
        self._value = value

    @property
    def dim_percentage(self) -> float:
        return self.store.load(self.get_key("dim_percentage"), default=0.01)

    @dim_percentage.setter
    def dim_percentage(self, value: float):
        if not isinstance(value, float):
            raise ValueError(
                VALUE_NOT_OF_TYPE(self.__class__.__name__, "value", value, float)
            )
        self.store.save(self.get_key("dim_percentage"), value)

    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, value: Direction):
        assert isinstance(value, Direction)
        self._direction = value

    def as_dict(self) -> dict:
        return OrderedDict(
            [
                ("dim_percentage", self.dim_percentage),
            ]
            + [(key, value) for key, value in super().as_dict().items()]
        )

    def loop(self):
        colour = self.colour.as_hsv()
        if self.change_colour:
            self._colour_selector_index = (self._colour_selector_index + 1) % len(self.colour_selectors)
        if self.direction.value == "down":
            if self.value is None:
                self.value = colour.value
            self.value = self.value - self.dim_percentage
            if self.value <= 0.0:
                colour.value = 0.0
                self.value = None
                self.direction.value = "up"
                if self.change_colour:
                    self._colour_selector_index = self._colour_selector_index + 1
                return
            colour.value = self.value
        elif self.direction.value == "up":
            if self.value is None:
                self.value = 0.0
            self.value = self.value + self.dim_percentage
            if self.value >= colour.value:
                self.value = None
                self.direction.value = "down"
                return
            colour.value = self.value
        self.leds.set_all(colour.as_rgb())

from typing import Optional
from collections import OrderedDict
from errors import VALUE_NOT_OF_TYPE
from objects.animation import Animation

import animations.normal


class Breath(animations.normal.Normal):
    ANIMATION: Animation = Animation("breath")
    _value = None

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

    def as_dict(self) -> dict:
        return OrderedDict(
            [("dim_percentage", self.dim_percentage)]
            + [(key, value) for key, value in super().as_dict().items()]
        )

    def loop(self):
        color = self.color.as_hsv()
        if self.value is None:
            self.value = color.value
        self.value = self.value - self.dim_percentage
        if self.value <= 0:
            self.value = None
            return
        color.value = self.value
        self.leds.set_all(color.as_rgb())

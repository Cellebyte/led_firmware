from typing import Optional
from collections import OrderedDict
from errors import VALUE_NOT_OF_TYPE
from objects.animation import Animation

import animations.base
import driver.store
import driver.color_store
import driver.led
from objects.direction import Direction
from objects.rgb import COLORS, RGB


class Breath(animations.base.BaseAnimation):
    ANIMATION: Animation = Animation("breath")
    _value = None
    _color_selector_index = 0
    _default_color_selectors = [1, 2, 3, 4, 0, 0, 0, 0, 0, 0]

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
    def color_selectors(self) -> list[int]:
        data = self.store.load(
            self.get_key("color_selectors"), default=self._default_color_selectors
        )
        assert isinstance(data, list)
        return data

    @color_selectors.setter
    def color_selectors(self, value: list[int]):
        if isinstance(value, list):
            assert len(value) <= 10, "Only 10 elements allowed value {} > 10".format(
                len(value)
            )
            self.store.save(self.get_key("color_selectors"), value)
        else:
            raise ValueError(
                VALUE_NOT_OF_TYPE(
                    "list", "color_selectors", value=value, allowed_type=list[int]
                )
            )

    @property
    def color(self) -> Optional[RGB]:
        color_store_index = self.color_selectors[self._color_selector_index]
        if color_store_index == 0:
            return None
        else:
            return self.color_store[color_store_index]

    def set_color_selector(self, index: int, value: int):
        data = self.color_selectors
        data[index] = value
        self.color_selectors = data

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
        return Direction.from_dict(
            self.store.load(
                self.get_key("direction"), default=Direction("up").as_dict()
            )
        )

    @direction.setter
    def direction(self, value: Direction):
        assert isinstance(value, Direction)
        self.store.save(self.get_key("direction"), value.as_dict())

    def as_dict(self) -> dict:
        return OrderedDict(
            [("dim_percentage", self.dim_percentage), ("direction", self.direction)]
            + [(key, value) for key, value in super().as_dict().items()]
        )

    def loop(self):
        if self.color is None:
            self._color_selector_index = 0
            return
        color = self.color.as_hsv()
        if self.direction == Direction("down"):
            if self.value is None:
                self.value = color.value
            self.value = self.value - self.dim_percentage
            color.value = self.value
            if self.value <= 0:
                self.value = None
                self.direction = Direction("up")
                self._color_selector_index = self._color_selector_index + 1
                return
        elif self.direction == Direction("up"):
            if self.value is None:
                self.value = 0
            self.value = self.value + self.dim_percentage
            if self.value >= color.value:
                self.value = None
                self.direction = Direction("down")
                self._color_selector_index = self._color_selector_index + 1
                return
            else:
                color.value = self.value
        self.leds.set_all(color.as_rgb())

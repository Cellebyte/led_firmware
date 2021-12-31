from collections import OrderedDict
import driver.colour_palettes
import driver.led
import driver.store
from errors import PUT_NOT_USEFUL, VALUE_NOT_OF_TYPE, VALUE_NOT_IN_RANGE
from objects.animation import Animation
from objects.rgb import COLOURS, RGB

import animations.base


class Normal(animations.base.BaseAnimation):
    ANIMATION: Animation = Animation("normal")
    _colour_selector_index = 0
    _colour_selectors_max_len = 1

    def __init__(
        self,
        store: driver.store.Store,
        leds: driver.led.LEDDriver,
        colour_palettes: driver.colour_palettes.ColourPalettes,
    ):
        super().__init__(store, leds)
        self.colour_palettes: driver.colour_palettes.ColourPalettes = colour_palettes
        self.found_key: bool = False

    @property
    def colour(self) -> RGB:
        print(self._colour_selector_index)
        colour = self.colour_palettes[self.palette_selector][
            self.colour_selectors[self._colour_selector_index]
        ]
        if colour is None:
            return COLOURS.BLACK
        return colour

    @property
    def palette_selector(self) -> int:
        data = self.store.load(self.get_key("palette_selector"), default=1)
        assert isinstance(data, int)
        return data

    @palette_selector.setter
    def palette_selector(self, value: int):
        assert isinstance(value, int), VALUE_NOT_OF_TYPE(
            self.__class__.__name__, "Key", value, int
        )
        assert 1 <= value <= self.colour_palettes.amount, VALUE_NOT_IN_RANGE(
            self.__class__.__name__, "Key", value, 1, self.colour_palettes.amount
        )
        self.store.save(self.get_key("palettte_selector"), value)

    @property
    def colour_selectors(self) -> list[int]:
        data = self.store.load(self.get_key("colour_selectors"), default=[1])
        assert isinstance(data, list)
        return data

    @colour_selectors.setter
    def colour_selectors(self, value: list[int]):
        if isinstance(value, list):
            if not len(value) <= self._colour_selectors_max_len:
                raise ValueError(VALUE_NOT_IN_RANGE(self.__class__.__name__, "colour_selectors", len(value), 0, self._colour_selectors_max_len))
            for item in value:
                self.colour_palettes[self.palette_selector].validate_key(item)
            self.store.save(self.get_key("colour_selectors"), list(value))
        else:
            raise ValueError(
                VALUE_NOT_OF_TYPE(
                    self.__class__.__name__,
                    "colour_selectors",
                    value=value,
                    allowed_type="list[int]",
                )
            )

    @property
    def change_colour(self) -> bool:
        data = self.store.load(self.get_key("change_colour"), default=False)
        assert isinstance(data, bool)
        return data

    @change_colour.setter
    def change_colour(self, value: bool):
        assert isinstance(value, bool)
        self.store.save(self.get_key("change_colour"), value)

    def update(self, data: dict):
        if (
            "colour_selectors" in data.keys()
            and data["colour_selectors"] != self.colour_selectors
        ):
            self.found_key = True
            self.colour_selectors = data["colour_selectors"]
        if (
            "palette_selector" in data.keys()
            and int(data["palette_selector"]) != self.palette_selector
        ):
            self.found_key = True
            self.palette_selector = int(data["palette_selector"])

        if "change_colour" in data.keys() and bool(
            data["change_colour"] != self.change_colour
        ):
            self.found_key = True
            self.change_colour = bool(data["change_colour"])
        if not self.found_key:
            self.found_key = False
            raise ValueError(PUT_NOT_USEFUL)

        return self

    def as_dict(self):
        return OrderedDict(
            [
                ("colour_selectors", self.colour_selectors),
                ("palette_selector", self.palette_selector),
                ("current_colour", self.colour.as_dict()),
                ("change_colour", self.change_colour),
            ]
        )

    def loop(self):
        self.leds.set_all(self.colour.normalize())

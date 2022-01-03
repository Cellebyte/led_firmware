from collections import OrderedDict
from typing import Optional

import objects.rgb
from errors import VALUE_NOT_IN_RANGE, VALUE_NOT_OF_TYPE

from .store import Store


class ColourPalette:
    default_name = "colours"

    def __init__(
        self,
        store: Store,
        slots: int = 10,
        palette: Optional[int] = None,
        default_colours: Optional[tuple] = None,
    ):
        self.slots = slots
        self.store = store
        self.palette = palette
        self.default_colours = default_colours
        if self.__getitem__(1) is None:
            self.__setitem__(1, objects.rgb.COLOURS.PURPLE)

    @property
    def name(self) -> str:
        if self.palette is not None:
            return "palette.{}.{}".format(self.palette, self.default_name)
        return self.default_name

    @property
    def default_colours(self) -> tuple:
        return self._default_colours

    @default_colours.setter
    def default_colours(self, value: Optional[tuple]):
        if value is None:
            self._default_colours = tuple([None for _ in range(self.slots)])
            return
        assert isinstance(value, tuple)
        assert self.slots == len(
            value
        ), "len(default_colours) [{}] does not match provided slots={}".format(
            len(value), self.slots
        )
        self._default_colours = value

    def get_key(self, key) -> str:
        return "{}.{}".format(self.name, key)

    def validate_key(self, key):
        assert isinstance(key, int), VALUE_NOT_OF_TYPE(
            self.__class__.__name__, "Key", key, int
        )
        assert 1 <= key <= self.slots, VALUE_NOT_IN_RANGE(
            self.__class__.__name__, "Key", key, 1, self.slots
        )

    def default(self, key: int) -> Optional[dict]:
        # This accomplishes the offset for the colour_palette store
        colour = self.default_colours[key - 1]
        if colour is not None:
            return colour.as_dict()
        return colour

    def validate_value(self, value: Optional[objects.rgb.RGB]):
        if value is None:
            return
        assert isinstance(value, (objects.rgb.RGB)), VALUE_NOT_OF_TYPE(
            self.__class__.__name__, self.name, value, objects.rgb.RGB
        )

    def __setitem__(self, key: int, value: objects.rgb.RGB):
        self.validate_key(key)
        self.validate_value(value)
        self.store.save(self.get_key(key), value.as_dict())

    def __getitem__(self, key: int) -> Optional[objects.rgb.RGB]:
        self.validate_key(key)
        colour = self.store.load(self.get_key(key), default=self.default(key))
        if colour is None:
            return None
        assert isinstance(colour, dict)
        return objects.rgb.RGB.from_dict(colour)

    def __iter__(self):
        for key in range(1, self.slots + 1):
            yield key

    def delete(self, key: int) -> Optional[objects.rgb.RGB]:
        self.validate_key(key)
        colour = self.store.delete(self.get_key(key))
        if colour is None:
            return None
        return objects.rgb.RGB.from_dict(colour)

    def as_dict(self):
        return OrderedDict(
            [
                # This type check is done in the comprehension as a filter function
                (str(key), self.__getitem__(key).as_dict())
                for key in self
                if isinstance(self.__getitem__(key), objects.rgb.RGB)
            ]
        )

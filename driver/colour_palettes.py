from collections import OrderedDict
import driver.colour_palette
import constants.colour_palettes
from errors import VALUE_NOT_IN_LIST, VALUE_NOT_IN_RANGE, VALUE_NOT_OF_TYPE

from .store import Store


class ColourPalettes:
    def __init__(self, store: Store, slots: int, amount: int = 1) -> None:
        self.amount = amount
        self.slots = slots
        # The last item gets default values for a rainbow
        self.palettes = {
            str(index): driver.colour_palette.colourPalette(
                store=store,
                slots=slots,
                palette=index,
                default_colours=(
                    None
                    if not index == self.amount
                    else constants.colour_palettes.RainbowColours
                ),
            )
            for index in range(1, self.amount + 1)
        }

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, value: int):
        assert isinstance(value, int), VALUE_NOT_OF_TYPE(
            self.__class__.__name__, "amount", value, int
        )
        assert 1 <= value <= 6, VALUE_NOT_IN_RANGE(
            self.__class__.__name__, "palette", value, 1, 6
        )
        self._amount = value

    def __iter__(self):
        for key in range(1, self.amount + 1):
            yield key

    def __getitem__(self, key: int) -> driver.colour_palette.colourPalette:
        assert str(key) in self.palettes.keys(), VALUE_NOT_IN_LIST(
            self.__class__.__name__, "Key", key, list(self.palettes.keys())
        )
        return self.palettes[str(key)]

    def as_dict(self):
        return OrderedDict(
            [(str(key), self.__getitem__(key).as_dict()) for key in self]
        )

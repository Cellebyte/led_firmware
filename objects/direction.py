from collections import OrderedDict
from errors import IS_REQUIRED, VALUE_NOT_IN_LIST


class Direction:
    SUPPORTED = ["up", "down"]
    _value = "up"

    def __init__(self, direction: str):
        self.value = direction

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        if value not in self.SUPPORTED:
            raise ValueError(
                VALUE_NOT_IN_LIST(
                    self.__class__.__name__,
                    self.__class__.__name__.lower(),
                    value,
                    self.SUPPORTED,
                )
            )
        self._value = value

    def __eq__(self, other: "Direction") -> bool:
        if isinstance(other, Direction):
            return self.value == other.value
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def as_dict(self):
        return OrderedDict([("{}".format(self.__class__.__name__.lower()), self.value)])

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data[cls.__name__.lower()])

    def __repr__(self) -> str:
        return "{}('{}')".format(self.__class__.__name__, self.value)

    def __hash__(self) -> int:
        return hash(self.value)

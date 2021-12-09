from collections import OrderedDict
from typing import Union
from errors import IS_REQUIRED, VALUE_NOT_IN_RANGE, VALUE_NOT_OF_TYPE

import objects.hsl
import objects.util


class RGB:
    MIN = 0
    MAX = 255

    def __init__(
        self, red: Union[int, float], green: Union[int, float], blue: Union[int, float]
    ):
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def validate_rgb_value(
        color, value: Union[int, float], class_name: str
    ) -> Union[int, float]:
        if not isinstance(
            value,
            (
                int,
                float,
            ),
        ):
            raise ValueError(VALUE_NOT_OF_TYPE(class_name, color, value, int))
        if not (RGB.MIN <= value <= RGB.MAX):
            raise ValueError(
                VALUE_NOT_IN_RANGE(class_name, color, value, RGB.MIN, RGB.MAX)
            )
        return value

    def normalize(self):
        self.red = round(self.red)
        self.green = round(self.green)
        self.blue = round(self.blue)
        return self

    @property
    def red(self) -> Union[int, float]:
        return self._red

    @red.setter
    def red(self, value: Union[int, float]):
        self._red = RGB.validate_rgb_value("red", value, self.__class__.__name__)

    @property
    def green(self) -> Union[int, float]:
        return self._green

    @green.setter
    def green(self, value: Union[int, float]):
        self._green = RGB.validate_rgb_value("green", value, self.__class__.__name__)

    @property
    def blue(self) -> Union[int, float]:
        return self._blue

    @blue.setter
    def blue(self, value: Union[int, float]):
        self._blue = RGB.validate_rgb_value("blue", value, self.__class__.__name__)

    def as_dict(self):
        return OrderedDict(
            [
                ("red", self.red),
                ("green", self.green),
                ("blue", self.blue),
            ]
        )

    def as_vector(self):
        return (self.red, self.green, self.blue)

    @classmethod
    def from_vector(cls, vector) -> "RGB":
        return cls(vector[0], vector[1], vector[2])

    @classmethod
    def from_dict(cls, data: dict) -> "RGB":
        return cls(data["red"], data["green"], data["blue"])

    def as_hsl(self) -> objects.hsl.HSL:
        return objects.util.rgb_to_hsl(self)

    def __add__(self, other: "RGB"):
        if isinstance(other, RGB):
            return RGB(
                self.red + other.red, self.green + other.green, self.blue + other.blue
            )
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    __radd__ = __add__

    def __eq__(self, other: "RGB") -> bool:
        if isinstance(other, RGB):
            return (
                self.red == other.red
                and self.green == other.green
                and self.blue == other.blue
            )
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def __sub__(self, other: "RGB"):
        if isinstance(other, RGB):
            return RGB(
                self.red - other.red, self.green - other.green, self.blue - other.blue
            )
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def __rsub__(self, other: "RGB"):
        if isinstance(other, RGB):
            return RGB(
                other.red - self.red, other.green - self.green, other.blue - self.blue
            )
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def __mul__(self, other: "RGB"):
        if isinstance(other, RGB):
            return RGB(
                self.red * other.red, self.green * other.green, self.blue * other.blue
            )
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    __rmul__ = __mul__

    def __truediv__(self, other: "RGB"):
        if isinstance(other, RGB):
            return RGB(
                self.red / other.red, self.green / other.green, self.blue / other.blue
            )
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def __repr__(self):
        return "{}({},{},{})".format(
            self.__class__.__name__, self.red, self.green, self.blue
        )


class COLORS:
    # non-colors
    BLACK = RGB(RGB.MIN, RGB.MIN, RGB.MIN)
    GRAY = RGB(RGB.MAX / 2, RGB.MAX / 2, RGB.MAX / 2).normalize()
    SILVER = RGB(192, 192, 192)
    WHITE = RGB(RGB.MAX, RGB.MAX, RGB.MAX)
    # shades with green
    LIME = RGB(RGB.MIN, RGB.MAX, RGB.MIN)
    GREEN = RGB(RGB.MIN, RGB.MAX / 2, RGB.MIN).normalize()
    # shades with red
    RED = RGB(RGB.MAX, RGB.MIN, RGB.MIN)
    MAROON = RGB(RGB.MAX / 2, RGB.MIN, RGB.MIN).normalize()
    # shades with blue
    BLUE = RGB(RGB.MIN, RGB.MIN, RGB.MAX)
    NAVY = RGB(RGB.MIN, RGB.MIN, RGB.MAX / 2).normalize()
    # without green
    MAGENTA = RGB(RGB.MAX, 0, RGB.MAX)
    PURPLE = RGB(RGB.MAX / 2, 0, RGB.MAX / 2).normalize()
    # without red
    TEAL = RGB(RGB.MIN, RGB.MAX / 2, RGB.MAX / 2).normalize()
    CYAN = RGB(RGB.MIN, RGB.MAX, RGB.MAX)
    # without blue
    OLIVE = RGB(RGB.MAX / 2, RGB.MAX / 2, RGB.MIN).normalize()
    YELLOW = RGB(RGB.MAX, RGB.MAX, RGB.MIN)

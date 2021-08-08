import objects.util as util
from errors import IS_REQUIRED, VALUE_NOT_IN_RANGE, VALUE_NOT_OF_TYPE

from objects.constants import RGB_BLUE, RGB_GREEN, RGB_RED

import objects.hsl


class RGB:
    MIN = 0
    MAX = 255

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def validate_rgb_value(color, value: int, class_name: str) -> int:
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
    def red(self) -> int:
        return self._red

    @red.setter
    def red(self, value: int):
        self._red = RGB.validate_rgb_value(RGB_RED, value, self.__class__.__name__)

    @property
    def green(self) -> int:
        return self._green

    @green.setter
    def green(self, value: int):
        self._green = RGB.validate_rgb_value(RGB_GREEN, value, self.__class__.__name__)

    @property
    def blue(self) -> int:
        return self._blue

    @blue.setter
    def blue(self, value: int):
        self._blue = RGB.validate_rgb_value(RGB_BLUE, value, self.__class__.__name__)

    def as_dict(self):
        return {
            RGB_RED: self.red,
            RGB_GREEN: self.green,
            RGB_BLUE: self.blue,
        }

    def as_vector(self):
        return (self.red, self.green, self.blue)

    def from_vector(self, vector):
        self.red = vector[0]
        self.green = vector[1]
        self.blue = vector[2]

    def as_hsl(self) -> objects.hsl.HSL:
        return util.rgb_to_hsl(self)

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


BLACK = RGB(RGB.MIN, RGB.MIN, RGB.MIN)
WHITE = RGB(RGB.MAX, RGB.MAX, RGB.MAX)
RED = RGB(RGB.MAX, RGB.MIN, RGB.MIN)
GREEN = RGB(RGB.MIN, RGB.MAX, RGB.MIN)
BLUE = RGB(RGB.MIN, RGB.MIN, RGB.MAX)
PURPLE = RGB(RGB.MAX / 2, 0, RGB.MAX / 2).normalize()

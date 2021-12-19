from typing import Tuple, Union
from errors import VALUE_NOT_IN_RANGE
import colorsys
import objects.hls
import objects.hsv
import objects.vector


class RGB(objects.vector.Vector):
    MIN = 0
    MAX = 255

    MAPPING = {"x": "red", "y": "green", "z": "blue"}

    normalization_vector = objects.vector.Vector(MAX, MAX, MAX)

    def __init__(
        self, red: Union[int, float], green: Union[int, float], blue: Union[int, float]
    ):
        self.red = red
        self.green = green
        self.blue = blue

    def validate(self, value, hint=""):
        value = super().validate(value, hint=hint)
        if not (RGB.MIN <= value <= RGB.MAX):
            raise ValueError(
                VALUE_NOT_IN_RANGE(
                    self.__class__.__name__, hint, value, RGB.MIN, RGB.MAX
                )
            )
        return value

    @property
    def red(self) -> Union[int, float]:
        return self.x

    @red.setter
    def red(self, value: Union[int, float]):
        self.x = self.validate(value, hint="red")

    @property
    def green(self) -> Union[int, float]:
        return self.y

    @green.setter
    def green(self, value: Union[int, float]):
        self.y = self.validate(value, hint="green")

    @property
    def blue(self) -> Union[int, float]:
        return self.z

    @blue.setter
    def blue(self, value: Union[int, float]):
        self.z = self.validate(value, hint="blue")

    def as_colorsys_tuple(self) -> Tuple[float, float, float]:
        return (self / self.normalization_vector).as_tuple()

    def as_hls(self) -> objects.hls.HLS:
        return objects.hls.HLS.from_tuple(
            (
                objects.vector.Vector.from_tuple(
                    colorsys.rgb_to_hls(*self.as_colorsys_tuple())
                )
                * objects.hls.HLS.normalization_vector
            ).as_tuple()
        )

    def as_hsv(self) -> objects.hsv.HSV:  #
        return objects.hsv.HSV.from_tuple(
            (
                objects.vector.Vector.from_tuple(
                    colorsys.rgb_to_hsv(*self.as_colorsys_tuple())
                )
                * objects.hsv.HSV.normalization_vector
            ).as_tuple()
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

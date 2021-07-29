import apiserver.util as util
import apiserver.objects.hsl


class RGB:
    MIN = 0
    MAX = 255

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def normalize(self):
        self.red = round(self.red)
        self.green = round(self.green)
        self.blue = round(self.blue)
        if self.red < self.MIN:
            self.red = self.MIN
        if self.green < self.MIN:
            self.green = self.MIN
        if self.blue < self.MIN:
            self.blue = self.MIN
        if self.red > self.MAX:
            self.red = self.MAX
        if self.green > self.MAX:
            self.green = self.MAX
        if self.blue > self.MAX:
            self.blue = self.MAX
        return self

    def as_dict(self):
        return {"red": self.red, "green": self.green, "blue": self.blue}

    def as_vector(self):
        return (self.red, self.green, self.blue)

    def from_vector(self, vector):
        self.red = vector[0]
        self.green = vector[1]
        self.blue = vector[2]

    def as_hsl(self) -> apiserver.objects.hsl.HSL:
        return util.rgb_to_hsl(self)

    def __add__(self, other: "RGB"):
        if isinstance(other, RGB):
            return RGB(
                self.red + other.red, self.green + other.green, self.blue + other.blue
            )
        else:
            raise ValueError("RGB is required")

    __radd__ = __add__

    def __eq__(self, other: "RGB") -> bool:
        if isinstance(other, RGB):
            return (
                self.red == other.red
                and self.green == other.green
                and self.blue == other.blue
            )
        else:
            raise ValueError("RGB is required")

    def __sub__(self, other: "RGB"):
        if isinstance(other, RGB):
            return RGB(
                self.red - other.red, self.green - other.green, self.blue - other.blue
            )
        else:
            raise ValueError("RGB is required")

    def __rsub__(self, other: "RGB"):
        if isinstance(other, RGB):
            return RGB(
                other.red - self.red, other.green - self.green, other.blue - self.blue
            )
        else:
            raise ValueError("RGB is required")

    def __mul__(self, other: "RGB"):
        if isinstance(other, RGB):
            return RGB(
                self.red * other.red, self.green * other.green, self.blue * other.blue
            )
        else:
            raise ValueError("RGB is required")

    __rmul__ = __mul__

    def __truediv__(self, other: "RGB"):
        if isinstance(other, RGB):
            return RGB(
                self.red / other.red, self.green / other.green, self.blue / other.blue
            )
        else:
            raise ValueError("RGB is required")

    def __repr__(self):
        return "RGB({},{},{})".format(self.red, self.green, self.blue)


BLACK = RGB(RGB.MIN, RGB.MIN, RGB.MIN)
WHITE = RGB(RGB.MAX, RGB.MAX, RGB.MAX)
RED = RGB(RGB.MAX, RGB.MIN, RGB.MIN)
GREEN = RGB(RGB.MIN, RGB.MAX, RGB.MIN)
BLUE = RGB(RGB.MIN, RGB.MIN, RGB.MAX)
PURPLE = RGB(RGB.MAX / 2, 0, RGB.MAX / 2)

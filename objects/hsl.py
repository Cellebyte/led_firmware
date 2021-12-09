from errors import IS_REQUIRED

import objects.rgb
import objects.util
from collections import OrderedDict


class HSL:
    def __init__(self, hue, saturation, luminance):
        self.hue = hue
        self.saturation = saturation
        self.luminance = luminance

    def as_rgb(self) -> objects.rgb.RGB:
        return objects.util.hsl_to_rgb(self)

    def as_dict(self) -> dict:
        return OrderedDict({
            "hue": self.hue,
            "saturation": self.saturation,
            "luminance": self.luminance,
        })

    def __sub__(self, other: "HSL"):
        if isinstance(other, HSL):
            return HSL(
                self.hue - other.hue,
                self.saturation - other.saturation,
                self.luminance - other.luminance,
            )
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def __rsub__(self, other: "HSL"):
        if isinstance(other, HSL):
            return HSL(
                other.hue - self.hue,
                other.saturation - self.saturation,
                other.luminance - self.luminance,
            )
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def __add__(self, other: "HSL"):
        if isinstance(other, HSL):
            return HSL(
                self.hue + other.hue,
                self.saturation + other.saturation,
                self.luminance + other.luminance,
            )
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    __radd__ = __add__

    def __repr__(self) -> str:
        return "{}({},{},{})".format(
            self.__class__.__name__, self.hue, self.saturation, self.luminance
        )

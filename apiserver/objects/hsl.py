from apiserver.constants import HSL_IS_REQUIRED
import apiserver.util
import apiserver.objects.rgb


class HSL:
    def __init__(self, hue, saturation, luminance):
        self.hue = hue
        self.saturation = saturation
        self.luminance = luminance

    def as_rgb(self) -> apiserver.objects.rgb.RGB:
        return apiserver.util.hsl_to_rgb(self)

    def as_dict(self) -> dict:
        return {
            "hue": self.hue,
            "saturation": self.saturation,
            "luminance": self.luminance,
        }

    def __sub__(self, other: "HSL"):
        if isinstance(other, HSL):
            return HSL(
                self.hue - other.hue,
                self.saturation - other.saturation,
                self.luminance - other.luminance,
            )
        else:
            raise ValueError(HSL_IS_REQUIRED)

    def __rsub__(self, other: "HSL"):
        if isinstance(other, HSL):
            return HSL(
                other.hue - self.hue,
                other.saturation - self.saturation,
                other.luminance - self.luminance,
            )
        else:
            raise ValueError(HSL_IS_REQUIRED)

    def __add__(self, other: "HSL"):
        if isinstance(other, HSL):
            return HSL(
                self.red + other.red, self.green + other.green, self.blue + other.blue
            )
        else:
            raise ValueError(HSL_IS_REQUIRED)

    __radd__ = __add__

    def __repr__(self) -> str:
        return "HSL({},{},{})".format(self.hue, self.saturation, self.luminance)

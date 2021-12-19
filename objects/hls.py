from typing import Union
from errors import IS_REQUIRED, VALUE_NOT_IN_RANGE
import colorsys
import objects.rgb
import objects.vector


class HLS(objects.vector.Vector):

    MAPPING = {
        "x": "hue",
        "y": "luminance",
        "z": "saturation",
    }
    normalization_vector = objects.vector.Vector(360, 1, 1)

    def __init__(self, hue, luminance, saturation):
        self.hue = hue
        self.luminance = luminance
        self.saturation = saturation

    @property
    def hue(self) -> Union[int, float]:
        return self.x

    @property
    def luminance(self) -> Union[int, float]:
        return self.y

    @property
    def saturation(self) -> Union[int, float]:
        return self.z

    @hue.setter
    def hue(self, value: Union[int, float]):
        if not (0 <= value <= 360):
            raise ValueError(
                VALUE_NOT_IN_RANGE(self.__class__.__name__, "hue", value, 0, 360)
            )
        self.x = value

    @luminance.setter
    def luminance(self, value: Union[int, float]):
        if not (0 <= value <= 1):
            raise ValueError(
                VALUE_NOT_IN_RANGE(self.__class__.__name__, "luminance", value, 0, 1)
            )
        self.y = value

    @saturation.setter
    def saturation(self, value: Union[int, float]):
        if not (0 <= value <= 1):
            raise ValueError(
                VALUE_NOT_IN_RANGE(self.__class__.__name__, "saturation", value, 0, 1)
            )
        self.z = value

    def as_rgb(self) -> objects.rgb.RGB:
        return objects.rgb.RGB.from_tuple(
            (
                objects.rgb.RGB.normalization_vector
                * objects.vector.Vector.from_tuple(
                    colorsys.hls_to_rgb(*(self / self.normalization_vector).as_tuple())
                )
            ).as_tuple()
        ).normalize()

    @classmethod
    def from_rgb(cls, rgb: objects.rgb.RGB) -> "HLS":
        if isinstance(rgb, objects.rgb.RGB):
            return rgb.as_hls()
        else:
            raise ValueError(IS_REQUIRED("RGB"))

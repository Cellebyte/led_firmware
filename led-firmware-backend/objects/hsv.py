import colorsys
from typing import Union

from errors import IS_REQUIRED, VALUE_NOT_IN_RANGE

import objects.rgb
import objects.vector


class HSV(objects.vector.Vector):

    MAPPING = {
        "x": "hue",
        "y": "saturation",
        "z": "value",
    }

    normalization_vector = objects.vector.Vector(360, 1, 1)

    def __init__(
        self,
        hue: Union[int, float],
        saturation: Union[int, float],
        value: Union[int, float],
    ):
        self.hue = hue
        self.saturation = saturation
        self.value = value

    @property
    def hue(self) -> Union[int, float]:
        return self.x

    @property
    def saturation(self) -> Union[int, float]:
        return self.y

    @property
    def value(self) -> Union[int, float]:
        return self.z

    @hue.setter
    def hue(self, value: Union[int, float]):
        if not (0 <= value <= 360):
            raise ValueError(
                VALUE_NOT_IN_RANGE(self.__class__.__name__, "hue", value, 0, 360)
            )
        self.x = value

    @saturation.setter
    def saturation(self, value: Union[int, float]):
        if not (0 <= value <= 1):
            raise ValueError(
                VALUE_NOT_IN_RANGE(self.__class__.__name__, "saturation", value, 0, 1)
            )
        self.y = value

    @value.setter
    def value(self, value: Union[int, float]):
        if not (0 <= value <= 1):
            raise ValueError(
                VALUE_NOT_IN_RANGE(self.__class__.__name__, "value", value, 0, 1)
            )
        self.z = value

    def as_rgb(self) -> objects.rgb.RGB:
        value = colorsys.hsv_to_rgb(*(self / self.normalization_vector).as_tuple())
        if value:
            return objects.rgb.RGB.from_tuple(
                (
                    objects.rgb.RGB.normalization_vector
                    * objects.vector.Vector.from_tuple(value)
                ).as_tuple()
            ).normalize()
        else:
            raise NotImplementedError(
                "colorsys.hsv_to_rgb(h,s,v) returned None but it should not"
            )

    @classmethod
    def from_rgb(cls, rgb: objects.rgb.RGB) -> "HSV":
        if isinstance(rgb, objects.rgb.RGB):
            return rgb.as_hsv()
        else:
            raise ValueError(IS_REQUIRED("RGB"))

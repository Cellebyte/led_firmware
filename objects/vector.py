from collections import OrderedDict
from typing import Union, Tuple
from errors import IS_REQUIRED, VALUE_NOT_OF_TYPE


class Vector:

    MAPPING = {"x": "x", "y": "y", "z": "z"}

    def validate(self, value: Union[int, float], hint: str = "") -> Union[int, float]:
        if not isinstance(value, (int, float)):
            raise ValueError(
                VALUE_NOT_OF_TYPE(
                    self.__class__.__name__, hint, value, Union[int, float]
                )
            )
        return value

    def __init__(
        self, x: Union[int, float], y: Union[int, float], z: Union[int, float]
    ):
        self.x = x
        self.y = y
        self.z = z

    @property
    def x(self) -> Union[int, float]:
        return self._x

    @x.setter
    def x(self, value: Union[int, float]):
        self._x = self.validate(value, hint=self.MAPPING["x"])

    @property
    def y(self) -> Union[int, float]:
        return self._y

    @y.setter
    def y(self, value: Union[int, float]):
        self._y = self.validate(value, hint=self.MAPPING["y"])

    @property
    def z(self) -> Union[int, float]:
        return self._z

    @z.setter
    def z(self, value: Union[int, float]):
        self._z = self.validate(value, hint=self.MAPPING["z"])

    def as_tuple(
        self,
    ) -> Tuple[Union[int, float], Union[int, float], Union[int, float]]:
        return (self.x, self.y, self.z)

    @classmethod
    def from_tuple(
        cls, obj: Tuple[Union[int, float], Union[int, float], Union[int, float]]
    ):
        if isinstance(obj, tuple) and len(obj) == 3:
            return cls(obj[0], obj[1], obj[2])
        else:
            raise ValueError(IS_REQUIRED("Tuple with 3 elements."))

    def as_dict(self) -> OrderedDict:
        return OrderedDict(
            [
                (self.MAPPING["x"], self.x),
                (self.MAPPING["y"], self.y),
                (self.MAPPING["z"], self.z),
            ]
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data[cls.MAPPING["x"]], data[cls.MAPPING["y"]], data[cls.MAPPING["z"]]
        )

    def __add__(self, other: "Vector"):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    __radd__ = __add__

    def __eq__(self, other: "Vector") -> bool:
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def __sub__(self, other: "Vector"):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def __rsub__(self, other: "Vector"):
        if isinstance(other, Vector):
            return Vector(other.x - self.x, other.y - self.y, other.z - self.z)
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def __mul__(self, other: "Vector"):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    __rmul__ = __mul__

    def __truediv__(self, other: "Vector"):
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def __repr__(self):
        return "{}({},{},{})".format(self.__class__.__name__, self.x, self.y, self.z)

    def normalize(self):
        self.x = round(self.x)
        self.y = round(self.y)
        self.z = round(self.z)
        return self

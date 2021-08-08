from errors import IS_REQUIRED, VALUE_NOT_IN_LIST

from objects.constants import (
    ANIMATION_BREATH,
    ANIMATION_MANUAL,
    ANIMATION_NORMAL,
    ANIMATION_OFF,
    ANIMATION_SNAKE,
)


class Animation:
    SUPPORTED = [
        ANIMATION_SNAKE,
        ANIMATION_NORMAL,
        ANIMATION_BREATH,
        ANIMATION_OFF,
        ANIMATION_MANUAL,
    ]

    def __init__(self, animation):
        if animation in self.SUPPORTED:
            self.value = animation
        else:
            raise ValueError(
                VALUE_NOT_IN_LIST(
                    self.__class__.__name__,
                    self.__class__.__name__.lower(),
                    animation,
                    self.SUPPORTED,
                )
            )

    def __eq__(self, other: "Animation") -> bool:
        if isinstance(other, Animation):
            return self.value == other.value
        else:
            raise ValueError(IS_REQUIRED(self.__class__.__name__))

    def as_dict(self):
        return {"{}".format(self.__class__.__name__.lower()): self.value}

    def __repr__(self) -> str:
        return "{}('{}')".format(self.__class__.__name__, self.value)

    def __hash__(self) -> int:
        return hash(self.value)

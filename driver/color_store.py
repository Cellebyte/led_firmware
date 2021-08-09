import objects.rgb
from errors import VALUE_NOT_IN_RANGE, VALUE_NOT_OF_TYPE

from .store import Store


class ColorStore:
    name: str = "colors"

    def __init__(self, store: Store, slots: int = 10):
        self.slots = slots
        self.store = store
        if self.__getitem__(1) is None:
            self.__setitem__(1, objects.rgb.PURPLE)

    def get_key(self, key):
        return "{}.{}".format(self.name, key)

    def validate_key(self, key):
        assert isinstance(key, int), VALUE_NOT_OF_TYPE(
            self.__class__.__name__, "Key", key, int
        )
        assert 1 <= key <= self.slots, VALUE_NOT_IN_RANGE(
            self.__class__.__name__, "Key", key, 1, self.slots
        )

    def validate_value(self, value):
        assert isinstance(value, (objects.rgb.RGB, None)), VALUE_NOT_OF_TYPE(
            self.__class__.__name__, self.name, value, objects.rgb.RGB
        )

    def __setitem__(self, key: int, value: objects.rgb.RGB):
        self.validate_key(key)
        self.validate_value(value)
        self.store.save(self.get_key(key), value.as_dict())

    def __getitem__(self, key: int) -> objects.rgb.RGB:
        self.validate_key(key)
        color = self.store.load(self.get_key(key), default=None)
        if color is not None:
            return objects.rgb.RGB(**color)
        return None

    def as_dict(self):
        return {key: self.__getitem__(key).as_dict() for key in range(1, self.slots + 1)}

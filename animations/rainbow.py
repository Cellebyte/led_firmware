from collections import OrderedDict
from errors import PUT_NOT_USEFUL, VALUE_NOT_OF_TYPE
from objects.animation import Animation
from animations import monotonic_ms, MS_PER_SECOND
from colorwheel import colorwheel
import animations.base


class Rainbow(animations.base.BaseAnimation):
    ANIMATION: Animation = Animation("rainbow")
    _position = 0
    _last_position = 0
    _last_update = 0

    @property
    def period(self) -> int:
        data = self.store.load(self.get_key("period"), default=5)
        assert isinstance(data, int)
        return data

    @period.setter
    def period(self, value: int):
        if not isinstance(value, int):
            raise ValueError(
                VALUE_NOT_OF_TYPE(self.__class__.__name__, "period", value, int)
            )
        self.store.save(self.get_key("period"), value)

    def update(self, data: dict):
        if "period" in data.keys() and data["period"] != self.period:
            self.found_key = True
            self.period = data["period"]
        if not self.found_key:
            self.found_key = False
            raise ValueError(PUT_NOT_USEFUL)

        return self

    def as_dict(self):
        return OrderedDict(
            [
                ("period", self.period),
            ]
        )

    def loop(self):
        period = int(self.period * MS_PER_SECOND)
        now = monotonic_ms()
        time_since_last_draw = now - self._last_update
        self._last_update = now
        pos = self._position = (self._position + time_since_last_draw) % period
        if pos < self._last_position:
            self._last_position = pos
        wheel_index = int((pos / period) * 256)
        self.leds.pixels[:] = [
            colorwheel((i + wheel_index) % 255) for i in range(self.leds.len_leds)
        ]
        self._wheel_index = wheel_index

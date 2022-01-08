
import driver.led
import driver.colour_palettes
from errors import VALUE_NOT_OF_TYPE
from objects.animation import Animation
from animations import monotonic_ms, MS_PER_SECOND
import animations.normal


class Cycle(animations.normal.Normal):
    ANIMATION: Animation = Animation("cycle")
    _colour_selectors_max_len = 16
    _position = 0
    _last_position = 0
    default_colour_selectors: list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

    @property
    def period(self) -> int:
        data = self.store.load(self.get_key('period'), default=5)
        assert isinstance(data, int)
        return data
    
    @period.setter
    def period(self, value: int):
        if not isinstance(value, int):
            raise ValueError(
                VALUE_NOT_OF_TYPE(self.__class__.__name__, 'period', value, int)
            )
        self.store.save(self.get_key('period'), value)
    @property
    def steps(self) -> int:
        data = self.store.load(self.get_key("steps"), default=1)
        assert isinstance(data, int)
        return data

    @steps.setter
    def steps(self, value: int):
        assert isinstance(value, int)
        self.store.save(self.get_key("steps"), value)

    @property
    def on_strip(self) -> bool:
        data = self.store.load(self.get_key('on_strip'), default=True)
        assert isinstance(data, bool)
        return data
    
    @on_strip.setter
    def on_strip(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError(
                VALUE_NOT_OF_TYPE(self.__class__.__name__, "on_strip", value, bool)
            )
        self.store.save(self.get_key('on_strip'), value)

    def _color_wheel_generator(self):
        period = int(self.period * MS_PER_SECOND)

        last_update = monotonic_ms()
        cycle_position = 0
        last_pos = 0
            now = monotonic_ms()
            time_since_last_draw = now - last_update
            last_update = now
            pos = cycle_position = (cycle_position + time_since_last_draw) % period
            if pos < last_pos:
                
            last_pos = pos
            wheel_index = int((pos / period) * 256)
            self.leds.pixels[:] = [
                colorwheel((i + wheel_index) % 255) for i in range(self.leds.len_leds)
            ]
            self._wheel_index = wheel_index

    def loop(self):
        if self.on_strip:
            self.leds.set_all(self.colour)
        else:

        if self.change_colour:
            self._colour_selector_index = (self._colour_selector_index + 1) % len(self.colour_selectors)

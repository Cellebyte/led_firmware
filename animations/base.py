import driver.led
import driver.store
from errors import IMPLEMENTATION_NEEDED
from objects.animation import Animation


class BaseAnimation:
    ANIMATION: Animation

    def __init__(
        self,
        store: driver.store.Store,
        leds: driver.led.LEDDriver,
    ):
        assert isinstance(store, driver.store.Store)
        assert isinstance(leds, driver.led.LEDDriver)
        self.store: driver.store.Store = store
        self.leds: driver.led.LEDDriver = leds

    def update(self, data: dict):
        raise NotImplementedError(IMPLEMENTATION_NEEDED)

    def as_dict(self):
        raise NotImplementedError(IMPLEMENTATION_NEEDED)

    def loop(self):
        raise NotImplementedError(IMPLEMENTATION_NEEDED)

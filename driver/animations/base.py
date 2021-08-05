from driver.constants import IMPLEMENTATION_NEEDED
from apiserver.objects.animation import Animation
import driver.store
import driver.led


class BaseAnimation:
    ANIMATION: Animation = None

    def __init__(self, store: driver.store.Store, leds: driver.led.LEDDriver):
        self.store: driver.store.Store = store
        self.leds: driver.led.LEDDriver = leds

    def update(self, data: dict):
        raise NotImplementedError(IMPLEMENTATION_NEEDED)

    def as_dict(self):
        raise NotImplementedError(IMPLEMENTATION_NEEDED)

    def loop(self):
        raise NotImplementedError(IMPLEMENTATION_NEEDED)

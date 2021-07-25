from apiserver.objects.animation import Animation
from driver.store import Store
from driver.led import LEDDriver


class BaseAnimation:
    ANIMATION: Animation = None

    def __init__(self, store: Store, leds: LEDDriver):
        self.store: Store = store
        self.leds: LEDDriver = leds

    def loop(self):
        raise NotImplementedError("This function needs to be implemented by a ChildAnimation")

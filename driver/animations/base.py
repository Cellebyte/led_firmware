from apiserver.objects.animation import Animation
import driver.store
import driver.led


class BaseAnimation:
    ANIMATION: Animation = None

    def __init__(self, store: driver.store.Store, leds: driver.led.LEDDriver):
        self.store: driver.store.Store = store
        self.leds: driver.led.LEDDriver = leds

    def loop(self):
        raise NotImplementedError("This function needs to be implemented by a ChildAnimation")

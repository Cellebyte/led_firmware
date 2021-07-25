import driver.animations.base
import gc

import uasyncio
from apiserver.objects.animation import Animation
from apiserver.objects.rgb import RGB, BLACK
from machine import Pin
from neopixel import NeoPixel

from driver.store import Store


class LEDDriver:

    LED_PIN = 4
    MAX_HUE = RGB.MAX

    def __init__(self, leds, meters, store, debug=False) -> None:
        self._len_leds = leds * meters
        self.pixels = NeoPixel(Pin(self.LED_PIN, Pin.OUT), self.len_leds)
        self.store: Store = store
        self.debug = debug
        self.animations = {}

    @property
    def len_leds(self) -> int:
        return self._len_leds

    @property
    def animation(self):
        return Animation(
            **self.store.load(
                "animation", default=Animation(animation="normal").as_dict()
            )
        )

    def register_animation(self, animation: driver.animations.base.BaseAnimation):
        assert isinstance(animation, driver.animations.base.BaseAnimation)
        self.animations[animation.ANIMATION] = animation

    @animation.setter
    def animation(self, value: Animation):
        assert isinstance(value, Animation)
        self.store.save("animation", value.as_dict())

    def write(self):
        self.pixels.write()

    async def start(self):
        count = 0
        while True:
            count += 1
            if count >= 60:
                count = 0
            await self.loop(count)
            gc.collect()
            await uasyncio.sleep_ms(10)

    def set(self, rgb: RGB, unit):
        self.pixels[unit] = rgb.as_vector()

    def set_all(self, rgb: RGB):
        for counter in range(self.len_leds):
            self.set(rgb, counter)

    def reset(self):
        self.set_all(BLACK)

    async def loop(self, count):
        try:
            self.animations[self.animation].loop()
            self.write()
        except KeyError:
            if count % 30 == 0:
                print("Animation('{}') is not implementd".format(self.animation.value))
        if self.debug:
            print("Hello from LED Driver  :: {}".format(count))

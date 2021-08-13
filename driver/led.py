import uasyncio
from objects.animation import Animation
from objects.rgb import BLACK, RGB
from machine import Pin
try:
    from neopixel import NeoPixel
except ImportError:
    from driver.neopixel import NeoPixel

import animations.base
from driver.store import Store


class LEDDriver:

    LED_PIN = 4
    MAX_HUE = RGB.MAX

    def __init__(self, leds, meters, store, debug=False) -> None:
        self._len_leds = int(round(leds * meters))
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
                self.__class__.__name__,
                default=Animation(animation="normal").as_dict(),
            )
        )

    def register_animation(self, animation: animations.base.BaseAnimation):
        assert isinstance(animation, animations.base.BaseAnimation)
        self.animations[animation.ANIMATION] = animation

    @animation.setter
    def animation(self, value: Animation):
        assert isinstance(value, Animation)
        self.store.save(self.__class__.__name__, value.as_dict())

    def write(self):
        self.pixels.write()

    async def start(self):
        count = 0
        while True:
            count += 1
            if count >= 60:
                count = 0
            await self.loop(count)
            await uasyncio.sleep_ms(5)

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
                print(
                    "{}('{}') is not implementd".format(
                        self.animation.__class__.__name__, self.animation.value
                    )
                )

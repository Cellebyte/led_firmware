import time

import animations.base
import uasyncio
from machine import Pin
from driver.custom_neopixel import CustomNeoPixel as NeoPixel
from objects.animation import Animation
from objects.rgb import COLOURS, RGB

from driver.store import Store


class LEDDriver:

    LED_PIN = 27
    MAX_HUE = RGB.MAX
    class ChannelMode:
        RGB = 0
        GRB = 1

    def __init__(self, leds, meters, store, debug=False, channel_mode=ChannelMode.RGB) -> None:
        self.pin = Pin(self.LED_PIN, Pin.OUT)
        self.pixels = NeoPixel(
            self.pin, int(round(leds * meters)), timing=(300, 1090, 1090, 320)
        )
        self.store: Store = store
        self.debug = debug
        self.channel_mode = channel_mode
        self.animations = {}

    @property
    def len_leds(self) -> int:
        return len(self.pixels)

    @property
    def animation(self) -> Animation:
        data = self.store.load(
            self.__class__.__name__,
            default=Animation(animation="normal").as_dict(),
        )
        assert isinstance(data, dict)
        return Animation.from_dict(data)

    def register_animation(self, animation: animations.base.BaseAnimation):
        assert isinstance(animation, animations.base.BaseAnimation)
        self.animations[animation.ANIMATION] = animation

    @animation.setter
    def animation(self, value: Animation):
        assert isinstance(value, Animation)
        self.store.save(self.__class__.__name__, value.as_dict())

    def write(self):
        self.pixels.write()
        # Needed due to datasheet of WS2815
        self.pin.off()
        time.sleep_us(300)

    async def start(self):
        count = 0
        while True:
            count += 1
            if count >= 60:
                count = 0
            await self.loop(count)
            await uasyncio.sleep_ms(5)

    def remap_color_channel(self, pixel: tuple[int, int, int]) -> tuple[int, int, int]:
        if self.channel_mode == self.ChannelMode.GRB:
            ## this swaps the color channel of red and green
            return (pixel[1],pixel[0],pixel[2])
        return pixel

    def set(self, rgb: RGB, unit):
        self.pixels[unit] = self.remap_color_channel(rgb.as_normalized_tuple())

    def get(self, unit) -> RGB:
        return RGB.from_tuple(self.remap_color_channel(self.pixels[unit]))

    def set_all(self, rgb: RGB):
        self.pixels.fill(self.remap_color_channel(rgb.as_normalized_tuple()))

    def reset(self):
        self.set_all(COLOURS.BLACK)
        self.write()

    async def loop(self, count):
        try:
            self.animations[self.animation].loop()
            self.write()
        except KeyError:
            if count % 30 == 0:
                print(
                    "{}('{}') is not implemented".format(
                        self.animation.__class__.__name__, self.animation.value
                    )
                )

from apiserver.objects.animation import Animation
from driver.animations.base import BaseAnimation
from ..util import add_tuple, multiply_tuple, sub_tuple


class Breath(BaseAnimation):
    ANIMATION = Animation('breath')

    # def dimm_desc(self, factor=5, steps=5):
    #     for _ in range(steps):
    #         self.dimm_all(factor=factor, ascending=False)
    #         self.write()

    # def dimm_asc(self, factor=5, steps=5):
    #     for _ in range(steps):
    #         self.dimm_all(factor=factor, ascending=True)
    #         self.write()

    def dimm_pixel(self, rgb, factor, ascending):
        factors = multiply_tuple(
            tuple([1 if color > 0 else 0 for color in rgb]), (factor, factor, factor)
        )
        if ascending:
            if any([color >= self.MAX_HUE for color in rgb]):
                return tuple(
                    [color if color < self.MAX_HUE else self.MAX_HUE for color in rgb]
                )
            return add_tuple(rgb, factors)
        else:
            if all([color < 0 for color in rgb]):
                return tuple([color if color > 0 else 0 for color in rgb])
            return sub_tuple(rgb, factors)

    def dimm_all(self, factor=5, ascending=False):
        for counter in range(self.len_leds):
            self.pixels[counter] = self.dimm_pixel(
                self.pixels[counter], factor=factor, ascending=ascending
            )

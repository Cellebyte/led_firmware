from objects.animation import Animation

from .base import BaseAnimation


class Off(BaseAnimation):
    ANIMATION: Animation = Animation("off")

    def loop(self):
        self.leds.reset()

    def as_dict(self):
        return {}

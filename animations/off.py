from objects.animation import Animation
from objects.constants import ANIMATION_OFF

from .base import BaseAnimation


class Off(BaseAnimation):
    ANIMATION = Animation(ANIMATION_OFF)

    def loop(self):
        self.leds.reset()

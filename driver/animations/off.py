
from apiserver.objects.animation import Animation
from driver.animations.base import BaseAnimation


class Off(BaseAnimation):
    ANIMATION = Animation('off')

    def loop(self):
        self.leds.reset()

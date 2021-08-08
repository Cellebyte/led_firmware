from objects.animation import Animation
from objects.constants import ANIMATION_BREATH

import animations.base


class Breath(animations.base.BaseAnimation):
    ANIMATION = Animation(ANIMATION_BREATH)

    def loop(self):
        pass

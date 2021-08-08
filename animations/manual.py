from objects.animation import Animation
from objects.constants import ANIMATION_MANUAL

import animations.base


class Manual(animations.base.BaseAnimation):
    ANIMATION: Animation = Animation(ANIMATION_MANUAL)

    def loop(self):
        pass

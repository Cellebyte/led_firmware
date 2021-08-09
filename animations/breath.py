from objects.animation import Animation

import animations.base


class Breath(animations.base.BaseAnimation):
    ANIMATION: Animation = Animation("breath")

    def loop(self):
        pass

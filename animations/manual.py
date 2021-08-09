from objects.animation import Animation

import animations.base


class Manual(animations.base.BaseAnimation):
    ANIMATION: Animation = Animation("manual")

    def loop(self):
        pass

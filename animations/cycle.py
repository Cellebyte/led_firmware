from collections import OrderedDict
from typing import Optional

from objects.animation import Animation

import animations.normal


class Cycle(animations.normal.Normal):
    ANIMATION: Animation = Animation("cycle")

    def loop(self):
        pass

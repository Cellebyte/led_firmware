import driver.animations.base
from apiserver.objects.animation import Animation


class Manual(driver.animations.base.BaseAnimation):
    ANIMATION: Animation = Animation("manual")

    def loop(self):
        pass

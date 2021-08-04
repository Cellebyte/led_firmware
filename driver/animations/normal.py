import driver.animations.base
from apiserver.objects.animation import Animation
from apiserver.objects.rgb import PURPLE, RGB


class Normal(driver.animations.base.BaseAnimation):
    ANIMATION = Animation("normal")

    @property
    def color(self) -> RGB:
        return RGB(
            **self.store.load(
                "{}.color".format(self.ANIMATION.value), default=PURPLE.as_dict()
            )
        )

    @color.setter
    def color(self, value: RGB):
        assert isinstance(value, RGB)
        self.store.save("{}.color".format(self.ANIMATION.value), value.as_dict())

    def loop(self):
        self.leds.set_all(self.color.normalize())

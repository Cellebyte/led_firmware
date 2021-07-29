from driver.animations.normal import Normal
from driver.led import LEDDriver
from apiserver.objects.animation import Animation
from driver.store import Store


class Snake(Normal):
    ANIMATION = Animation("snake")

    def __init__(self, store: Store, leds: LEDDriver):
        self.position = 0
        self.end_position = 0
        super().__init__(store, leds)

    @property
    def steps(self) -> int:
        return self.store.load("{}.steps".format(self.ANIMATION.value), default=1)

    @steps.setter
    def steps(self, value: int):
        assert isinstance(value, int)
        self.store.save("{}.steps".format(self.ANIMATION.value), value)

    @property
    def length(self) -> int:
        return self.store.load("{}.length".format(self.ANIMATION.value), default=30)

    @length.setter
    def length(self, value: int):
        assert isinstance(value, int)
        self.store.save("{}.length".format(self.ANIMATION.value), value)

    def loop(self):
        self.leds.reset()
        if self.position <= self.length:
            for i in range(0, self.position):
                self.leds.set(self.color, i)
        elif self.position > self.length and self.position <= self.leds.len_leds:
            self.end_position = 0
            for i in range(self.position - self.length, self.position):
                self.leds.set(self.color, i)
        elif self.position > self.leds.len_leds:
            self.end_position = self.position
            self.position = -1
        if self.end_position > self.leds.len_leds:
            for i in range(self.end_position - self.length, self.leds.len_leds):
                self.leds.set(self.color, i)
            self.end_position += self.steps
        self.position += self.steps

from driver.animations.normal import Normal
from driver.led import LEDDriver
from apiserver.objects.animation import Animation
from apiserver.objects.rgb import BLACK
from driver.store import Store


class Snake(Normal):
    ANIMATION = Animation("snake")

    def __init__(self, store: Store, leds: LEDDriver):
        self.position = 0
        super().__init__(store, leds)

    @property
    def length(self):
        return self.store.load("{}.length".format(self.ANIMATION.value), default=30)

    @length.setter
    def length(self, value: int):
        assert isinstance(value, int)
        self.store.save("{}.length".format(self.ANIMATION.value), value)

    def loop(self):
        if self.position - self.length - 1 == self.leds.len_leds and self.position != 0:
            self.position = 0
        elif self.position <= self.length:
            for i in range(0, self.position):
                self.leds.set(self.color, i)
        elif self.position > self.length and self.position <= self.leds.len_leds:
            for i in range(self.position - self.length, self.position):
                self.leds.set(self.color, i)
            for i in range(0, self.position - self.length):
                self.leds.set(BLACK, i)
        elif self.position > self.leds.len_leds:
            for i in range(self.position - self.length, self.leds.len_leds):
                self.leds.set(self.color, i)
            for i in range(0, self.position - self.length):
                self.leds.set(BLACK, i)
        self.position += 1

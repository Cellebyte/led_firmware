from machine import SPI


class MySPI(SPI):
    def __enter__(self):
        self.init()
        return self

    def __exit__(self, *exc):
        return self.deinit

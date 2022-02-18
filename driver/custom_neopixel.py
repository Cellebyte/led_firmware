from typing import Union

from neopixel import NeoPixel


class CustomNeoPixel(NeoPixel):
    def __setitem__(
        self,
        i: Union[int, slice],
        v: Union[
            list[tuple[int, int, int]],
            tuple[int, int, int],
        ],
    ):
        if isinstance(i, slice):
            start, stop, step = i.indices(self.n)
            for val_i, in_i in enumerate(range(start, stop, step)):
                super().__setitem__(in_i, v[val_i])
        else:
            super().__setitem__(i, v)

    def __getitem__(
        self, i: Union[int, slice]
    ) -> Union[list[tuple[int, int, int]], tuple[int, int, int],]:
        if isinstance(i, slice):
            out: list = []
            for in_i in range(*i.indices(len(self.buf) // self.bpp)):
                out.append(super().__getitem__(in_i))
            return out
        return super().__getitem__(i)

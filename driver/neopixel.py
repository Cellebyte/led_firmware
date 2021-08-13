import time
import rp2

# PIO state machine for RGB. Pulls 24 bits (rgb -> 3 * 8bit) automatically
@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_LOW,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=24,
)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, "do_zero").side(1)[T1 - 1]
    jmp("bitloop").side(1)[T2 - 1]
    label("do_zero")
    nop().side(0)[T2 - 1]
    wrap()


# PIO state machine for RGBW. Pulls 32 bits (rgbw -> 4 * 8bit) automatically
@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_LOW,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=32,
)
def sk6812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, "do_zero").side(1)[T1 - 1]
    jmp("bitloop").side(1)[T2 - 1]
    label("do_zero")
    nop().side(0)[T2 - 1]
    wrap()


class NeoPixel:
    ORDER = (1, 0, 2, 3)
    STATE_MACHINE = 0

    def __init__(self, pin, n, bpp=3, timing=1):
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        self.pin.init(pin.OUT)
        if self.bpp == 4:
            self.sm = rp2.StateMachine(
                self.STATE_MACHINE, sk6812, freq=8000000, sideset_base=self.pin
            )
        elif self.bpp == 3:
            self.sm = rp2.StateMachine(
                self.STATE_MACHINE, ws2812, freq=8000000, sideset_base=self.pin
            )
        else:
            NotImplementedError(
                "Color Space with bpp {} not implemented.".format(self.bpp)
            )
        self.sm.active(1)
        self.timing = timing

    def __len__(self):
        return self.n

    def __setitem__(self, index, val):
        offset = index * self.bpp
        for i in range(self.bpp):
            self.buf[offset + self.ORDER[i]] = val[i]

    def __getitem__(self, index):
        offset = index * self.bpp
        return tuple(self.buf[offset + self.ORDER[i]] for i in range(self.bpp))

    def fill(self, color):
        for i in range(self.n):
            self[i] = color
        time.sleep(self.timing)

    def write(self):
        for i in range(self.n):
            self.sm.put(self[i])
        time.sleep(self.timing)

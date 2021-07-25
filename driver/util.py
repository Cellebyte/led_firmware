import gc
import os

import micropython


def sub_tuple(a, b):
    return tuple(map(lambda x, y: x - y, a, b))


def add_tuple(a, b):
    return tuple(map(lambda x, y: x + y, a, b))


def multiply_tuple(a, b):
    return tuple(map(lambda x, y: x * y, a, b))


async def gc_info():
    print("--------------------------------------------------")
    print("Memory allocated: {} bytes".format(gc.mem_alloc()))
    print("Memory free:      {} bytes".format(gc.mem_free()))
    print("--------------------------------------------------")
    print(micropython.mem_info())
    print("--------------------------------------------------")


def df():
    s = os.statvfs("//")
    return "{0} MB".format((s[0] * s[3]) / 1048576)

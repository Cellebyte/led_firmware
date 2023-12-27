# SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Timing for Adafruit LED Animation library.
Author(s): Kattni Rembor
"""

try:
    from micropython import const
except ImportError:

    def const(value):  # pylint: disable=missing-docstring
        return value


import time


def monotonic_ms():
    return time.ticks_ms()


MS_PER_SECOND = const(1000)

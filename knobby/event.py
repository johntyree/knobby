#!/usr/bin/env python3
# coding: utf8

from __future__ import division, print_function

import sys
import os
import struct as st
import itertools as it

from .utils import as_binary, as_hex


# struct {
#   timeval {int, int}
#   unsigned long
#   unsigned long
# }
event_fmt = "@iiLL"


class Event(object):

    struct = st.Struct(event_fmt)

    def __init__(self, seconds, microseconds, second, thoid):
        self.time = seconds + (microseconds * 1e-6)
        self.b = second
        self.c = thoid
        self._hex_print = True

    def __repr__(self):
        fmt = """Event(time={time}, b={b}, c={c})"""
        return fmt.format(**vars(self))

    def __str__(self):
        if self._hex_print:
            fmt = as_hex
        else:
            fmt = as_binary
        d = []
        d.append(repr(self))
        d.append(fmt(self.b))
        d.append(fmt(self.c))
        return '{:50} {} {}'.format(*d)

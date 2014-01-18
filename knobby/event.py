#!/usr/bin/env python3
# coding: utf8

from __future__ import division, print_function

import struct as st

from .utils import as_binary, as_hex


# struct {
#   timeval {long sec, long usec}
#   int id
#   int data
# }
event_fmt = "@LLii"


class Event(object):

    struct = st.Struct(event_fmt)

    BUTTON = 0x01000001
    TURN   = 0x00070002

    def __init__(self, seconds, microseconds, event_id, data):
        self.seconds = seconds
        self.microseconds = microseconds
        self.id = event_id
        self.data = data
        self._hex_print = True

    @property
    def time(self):
        return self.seconds + (self.microseconds * 1e-6)

    def __repr__(self):
        fmt = ("Event(sec={seconds}"
               ", usec={microseconds:06}"
               ", id={id:08x}"
               ", data={data:08x})")
        d = vars(self)
        d['time'] = self.time
        return fmt.format(**d)

    def __str__(self):
        if self._hex_print:
            fmt = as_hex
        else:
            fmt = as_binary
        d = []
        d.append(repr(self))
        d.append(fmt(self.id))
        d.append(fmt(self.data))
        return '{:60} {} {}'.format(*d)

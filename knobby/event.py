#!/usr/bin/env python3
# coding: utf8

from __future__ import division, print_function

import struct as st

from .utils import as_binary, as_hex, reverse_dict, clamp


# struct {
#   timeval {long sec, long usec}
#   unsigned int id
#   int data
# }
event_fmt = "@LLIi"

EVENT_BY_NAME = {'button': 0x01000001,
                 'end': 0x0,
                 'turn': 0x00070002}
EVENT_BY_ID = reverse_dict(EVENT_BY_NAME, unique=True)


class Event(object):
    """ An Event from the device. """

    struct = st.Struct(event_fmt)

    def __init__(self, seconds, microseconds, event_id, data):
        self.seconds = seconds
        self.microseconds = microseconds
        self.id = event_id
        self.data = data
        self._hex_print = True

    @property
    def name(self):
        """ Return the name of this event as listed in EVENT_BY_NAME. """
        return EVENT_BY_ID.get(self.id)

    @property
    def time(self):
        """ Return a float of the time since the epoch of the creation
        of this event. """
        return self.seconds + (self.microseconds * 1e-6)

    def __repr__(self):
        fmt = ("Event(sec={seconds}"
               ", usec={microseconds:06}"
               ", id={id:08x}"
               ", data={data: 08x})")
        d = vars(self)
        d['time'] = self.time
        return fmt.format(**d)

    def describe(self):
        """ Return a pretty description of the Event."""
        ret = []
        if self.name:
            ret.append(self.name.title())
            if self.name == 'button':
                ret.append(('released', 'pressed')[clamp(self.data, 0, 1)])
            elif self.name == 'turn':
                direction = clamp(self.data, 0, 1)
                ret.append(('counter-clockwise', 'clockwise')[direction])
                units = abs(self.data)
                s = 's' if units != 1 else ''
                ret.append("{} unit{}".format(units, s))
        return ' '.join(ret)

    def __str__(self):
        fmt = as_hex if self._hex_print else as_binary
        d = []
        d.append("{:60}".format(repr(self)))
        d.append(fmt(self.id))
        d.append(fmt(self.data))
        d.append(self.describe())
        return ' '.join(d)

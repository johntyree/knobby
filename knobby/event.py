#!/usr/bin/env python3
# coding: utf8

from __future__ import division, print_function

import functools as ft
import itertools as it
import struct as st

from .utils import (
    as_binary, as_hex, reverse_dict, clamp, struct_stream, try_repeatedly)


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


class EventHandler(object):
    """Read and process a stream of events.

    callback : callable
    callback is called on each event.

    """

    def __init__(self, callback=print, source_filename='/dev/powermate'):
        """ Initialize the handler and attempt to open the data source.
        Give up after 5 tries.
        """
        self.callback = callback
        self.source_filename = source_filename
        self._fin = None

    def fin():
        def fget(self):
            return self._fin
        def fset(self, value):
            if value == '-':
                value = '/dev/stdin'
            if self.fin:
                del self.fin
            open_file = ft.partial(open, value, 'rb')
            self._fin = try_repeatedly(open_file, OSError, 5)
        def fdel(self):
            self._fin.close()
            del self._fin
        return locals()
    fin = property(**fin())

    def process(self, n=None):
        """ Wait for events and process them as they come. Return immediately
        if the callback returns True.

        n : int
            Limit processing to `n` events.
        """
        if not self.source_filename:
            raise ValueError("Source file `Event.fin` not set")

        self.fin = self.source_filename

        chunks = struct_stream(Event, self.fin)
        if n is not None:
            chunks = it.islice(chunks, n)
        for event in chunks:
            ret = self.callback(event)
            if ret:
                return ret

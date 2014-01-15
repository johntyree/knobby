#!/usr/bin/env python3
# coding: utf8

from __future__ import division, print_function

import sys
import os
import itertools as it
import struct

from utils import (
    struct_stream, open_data, chunks_of, chunks_of_buf, as_binary, as_hex)

# struct {
#   timeval {int, int}
#   long
#   long
# }
event_fmt = "@iill"


class Event(object):

    struct = struct.Struct(event_fmt)

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



def main():
    """Run main."""
    event = struct.Struct(event_fmt)
    filename = sys.argv[1] if sys.argv[1:] else 'push_button'
    starttime = None
    with open_data(filename) as fin:
        starts, stops = zip(*list(chunks_of(2, struct_stream(Event, fin))))
        print("Starts:")
        for event in starts:
            starttime = starttime or event.time
            event.time -= starttime
            print(event)
        print("Stops:")
        for event in stops:
            starttime = starttime or event.time
            event.time -= starttime
            print(event)
    return 0

if __name__ == '__main__':
    main()

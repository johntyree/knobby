#!/usr/bin/env python
# coding: utf8

from __future__ import division, print_function

import sys
import os
import itertools as it
import struct

from utils import struct_stream, open_data, chunks_of

# struct {
#   timeval {int, int}
#   long
#   long
# }
event_fmt = "@iill"


class Event(object):

    struct = struct.Struct(event_fmt)

    def __init__(self, seconds, microseconds, second, thoid):
        self.time = seconds + microseconds / 1e-6
        self.b = seconds
        self.c = thoid

    def __repr__(self):
        fmt = """Event(time={time}, b={b}, c={c})"""
        return fmt.format(**vars(self))

    def __str__(self):
        d = []
        d.append(repr(self))
        d.append("{:0>64b}".format(self.b))
        d.append("{:0>64b}".format(self.c))
        return '\n\t'.join(d)


def main():
    """Run main."""
    event = struct.Struct(event_fmt)
    filename = sys.argv[1] if sys.argv[1:] else 'push_button'
    with open_data(filename) as fin:
        for event in struct_stream(Event, fin):
            print(event)
    return 0

if __name__ == '__main__':
    main()

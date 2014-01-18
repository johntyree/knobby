#!/usr/bin/env python3
# coding: utf8

from __future__ import division, print_function

import itertools as it
import optparse
import sys

from .event import Event
from .utils import struct_stream


def parse_args(argv=sys.argv):
    o = optparse.OptionParser()
    o.add_option('-n', '--num-events', dest='n', type=int)
    o.add_option('-f', '--input-file', default='-', dest='filename',
                 help="The event file.")
    opts, args = o.parse_args(argv)
    return opts, args


def process(fin, callback=print, n=None):
    """Read and process a stream of events.

    n : int
        Limit processing to `n` events.

    callback : callable
        callback is called on each event.

    """
    chunks = struct_stream(Event, fin)
    if n is not None:
        chunks = it.islice(chunks, n)
    for event in chunks:
        ret = callback(event)
        if not ret:
            return ret


def main():
    """Run main."""
    opts, _ =parse_args()
    if opts.filename != '-':
        with open(opts.filename, 'rb') as fin:
            process(fin, opts.n)
    else:
        process(sys.stdin, opts.n)
    return 0


if __name__ == '__main__':
    main()

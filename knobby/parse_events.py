#!/usr/bin/env python3
# coding: utf8

from __future__ import division, print_function

import itertools as it
import optparse
import sys

from .event import Event
from .utils import struct_stream, chunks_of


def parse_args(argv=sys.argv):
    o = optparse.OptionParser()
    o.add_option('-n', '--num-events', dest='n', type=int)
    o.add_option('-f', '--input-file', default='-', dest='filename',
                 help="The event file.")
    opts, args = o.parse_args(argv)
    # o.file = args[0] if args else 'push_button'
    return opts, args


def process(fin, n=None):
    starttime = None
    chunks = chunks_of(2, struct_stream(Event, fin))
    if n is not None:
        chunks = it.islice(chunks, n)
    starts, stops = zip(*tuple(chunks))
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

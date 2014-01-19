#!/usr/bin/env python3
# coding: utf8

from __future__ import division, print_function

import functools as ft
import optparse
import sys

from .event import EventHandler
from .utils import try_repeatedly


def parse_args(argv=sys.argv):
    o = optparse.OptionParser()
    o.add_option('-n', '--num-events', dest='n', type=int)
    o.add_option('-f', '--input-file', default='/dev/powermate',
                 dest='filename', help="The PowerMate character device.")
    opts, args = o.parse_args(argv)
    if opts.filename == '-':
        opts.filename = '/dev/stdin'
    return opts, args


def main(handler=None):
    """Run the given `EventHandler` or a default one if None given."""
    opts, _ = parse_args()
    handler = handler or EventHandler()
    if not opts.n:
        try_repeatedly(ft.partial(handler.process, n=opts.n), OSError, 5)
    else:
        handler.process(n=opts.n)
    return 0


if __name__ == '__main__':
    main()

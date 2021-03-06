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
    o.add_option('-q', '--quiet', dest='verbose', action="store_false",
                 default=True, help="Don't print events.")
    opts, args = o.parse_args(argv)
    if opts.filename == '-':
        opts.filename = '/dev/stdin'
    return opts, args


def main(handler=None, argv=None):
    """Run the given `EventHandler` or a default one if None given."""
    argv = sys.argv if argv is None else argv
    opts, _ = parse_args(argv)
    handler = handler or EventHandler()
    if not opts.n:
        try_repeatedly(
            ft.partial(handler.process, n=opts.n, verbose=opts.verbose),
            OSError, 5)
    else:
        handler.process(n=opts.n, verbose=opts.verbose)
    return 0


if __name__ == '__main__':
    main()

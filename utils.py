#!/usr/bin/env python3
# coding: utf8

from __future__ import division, print_function

import sys
import os
import itertools as it


def struct_stream(klass, buf):
    """ Return an iterator that produces ``klass`` objects. The
    ``klass`` constructor should take a tuple of values as produced
    by struct.unpack().
    """
    sz = klass.struct.size
    unpack = klass.struct.unpack
    for chunk in chunks_of(sz, buf):
        data = unpack(chunk)
        yield klass(*data)


def open_data(filename):
    return open(os.path.join('events', filename), 'rb')


def chunks_of(sz, buf):
    """ For a file like object supporting .read(), return an iterator
    that produces size ``sz`` byte chunks
    """
    data = buf.read(sz)
    while data:
        # Pad to chunk size
        data += bytes(sz - len(data))
        yield data
        data = buf.read(sz)

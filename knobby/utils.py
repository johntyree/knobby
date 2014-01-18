#!/usr/bin/env python3
# coding: utf8

from __future__ import division, print_function


def struct_stream(klass, buf):
    """ Return an iterator that produces ``klass`` objects. The
    ``klass`` constructor should take a tuple of values as produced
    by struct.unpack().
    """
    sz = klass.struct.size
    unpack = klass.struct.unpack
    for chunk in chunks_of_buf(sz, buf):
        data = unpack(chunk)
        yield klass(*data)


def chunks_of(sz, it):
    it = iter(it)
    try:
        while sz > 0:  # Non-positive sizes are useless
            ret = []
            count = sz
            while count:
                count -= 1
                ret.append(next(it))
            if ret:
                yield tuple(ret)
    except StopIteration:
        if ret:
            yield tuple(ret)


def chunks_of_buf(sz, buf):
    """ For a file like object supporting .read(), return an iterator
    that produces size ``sz`` byte chunks
    """
    data = buf.read(sz)
    while data:
        # Pad to chunk size
        data += bytes(sz - len(data))
        yield data
        data = buf.read(sz)


def chunks_of_str(sz, string):
    return ' '.join(''.join(c) for c in chunks_of(sz, string))


def reverse_dict(d, unique=False):
    if unique:
        ret = {v: k for k, v in d.items()}
    else:
        ret = {}
        for k, v in d.items():
            ret.setdefault(k, []).append(v)
    return ret


def as_binary(val, sz=32):
    string = "{:0={sz}b}".format(val, sz=sz)
    return chunks_of_str(8, string)


def as_hex(val, sz=32):
    string = "{:0={sz}x}".format(val, sz=sz//4)
    return chunks_of_str(4, string)


def intersperse(elem, it):
    it = iter(it)
    yield next(it)
    for i in it:
        yield elem
        yield i


def diff_binary(a, b):
    s1 = as_binary(a)
    s2 = as_binary(b)
    return string_diff(s1, s2)


def string_diff(s1, s2):
    chars = [' ' if a == b else '|' for a, b in zip(s1, s2)]
    return ''.join(chars)

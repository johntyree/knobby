#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess


class Skipper(object):

    """ The Skipper lets us swallow repeated events without missing single
    event occurrences. """

    def __init__(self, do_not_skips):
        """ Event types *not* included in `do_not_skips` will need to be
        repeated `self.go` times before any action is taken. """
        self.counter = 0
        self.cmd = None
        self.do_not_skips = do_not_skips
        self.go = 4

    def run(self, cmd):
        if cmd in self.do_not_skips:
            self.counter = 0
            ret = subprocess.call(cmd)
            if ret:
                return ret
        else:
            if cmd == self.cmd:
                self.counter += 1
            else:
                self.cmd = cmd
                self.counter = 1
            while self.counter >= self.go:
                self.counter -= self.go
                ret = subprocess.call(self.cmd)
                if ret:
                    return ret
        return 0

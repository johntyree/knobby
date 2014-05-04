#!/usr/bin/env python
# coding: utf8
""" A fart button. """

from __future__ import division, print_function

import subprocess

from ..event import EventHandler
from ..main import main


class Skipper(object):

    def __init__(self, do_not_skips):
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

handler = Skipper([['fart']])


def callback(event):
    if event.name == 'button' and event.data == 1:
        cmd = ['fart']
        ret = handler.run(cmd)
        if ret:
            return ret
    elif event.name == 'turn':
        cmd = ['pulseaudio-ctl']
        cmd.append(('down', 'up')[event.data > 0])
        for i in range(abs(event.data)):
            ret = handler.run(cmd)
            if ret:
                return ret
    return False


fart_handler = EventHandler(callback=callback)

if __name__ == '__main__':
    main(handler=fart_handler)

#!/usr/bin/env python
# coding: utf8
"""An example script for controlling the system audio with knobby.

Turning the knob left and right increases and decreases the volume. Pressing
the button toggles mute.

"""

from __future__ import division, print_function

import subprocess

from ..event import EventHandler
from ..main import main

VOL_UP = ['pulseaudio-ctl', 'up']
VOL_DOWN = ['pulseaudio-ctl', 'down']
MUTE = ['pulseaudio-ctl', 'mute']


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

# We don't want to have to press mute more than once
handler = Skipper([['pulseaudio-ctl mute']])


def volume_callback(event):
    """ React to a knob event by adjusting the volume. """
    if event.name == 'button' and event.data == 0:
        handler.run(MUTE)
    elif event.name == 'turn':
        cmd = VOL_UP if event.data > 0 else VOL_DOWN
        for i in range(abs(event.data)):
            handler.run(cmd)
    return False


volume_control_handler = EventHandler(callback=volume_callback)

if __name__ == '__main__':
    main(handler=volume_control_handler)

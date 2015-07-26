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


handler = Skipper(['amixer -c 0 set PCM toggle'.split()])


def volume_callback(event):
    cmd = ['amixer', '-c', '0', 'set', 'PCM']
    if event.name == 'button' and event.data == 0:
        cmd.append('toggle')
        print(cmd)
        handler.run(cmd)
    elif event.name == 'turn':
        cmd.append(('5dB-', '5dB+')[event.data > 0])
        for i in range(abs(event.data)):
            handler.run(cmd)
    return False


volume_control_handler = EventHandler(callback=volume_callback)

if __name__ == '__main__':
    main(handler=volume_control_handler)

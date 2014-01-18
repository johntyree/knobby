#!/usr/bin/env python
# coding: utf8
"""An example script for controlling the system audio with knobby.

Turning the knob left and right increases and decreases the volume. Pressing
the button toggles mute.

"""

from __future__ import division, print_function

import subprocess

from .event import EventHandler
from .main import main


def volume_callback(event):
    print(event)
    cmd = ['pulseaudio-ctl']
    if event.name == 'button' and event.data == 0:
        cmd.append('mute')
        if subprocess.call(cmd):
            return 1
    elif event.name == 'turn':
        cmd.append(('down', 'up')[event.data > 0])
        for i in range(abs(event.data)):
            if subprocess.call(cmd):
                return 1
    return False


if __name__ == '__main__':
    handler = EventHandler(callback=volume_callback)
    main(handler=handler)

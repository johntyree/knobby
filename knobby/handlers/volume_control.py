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


def volume_callback(event):
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


volume_control_handler = EventHandler(callback=volume_callback)

if __name__ == '__main__':
    main(handler=volume_control_handler)

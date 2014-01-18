#!/usr/bin/env python
# coding: utf8
"""An example script for controlling the system audio with knobby.

Turning the knob left and right increases and decreases the volume. Pressing
the button toggles mute.

"""

from __future__ import division, print_function

import subprocess
import time

from .parse_events import process


def volume_callback(event):
    print(event)
    cmd = ['pulseaudio-ctl']
    if event.name == 'button' and event.data == 0:
        cmd.append('mute')
        if subprocess.call(cmd):
            return False
    elif event.name == 'turn':
        cmd.append(('down', 'up')[event.data > 0])
        for i in range(abs(event.data)):
            if subprocess.call(cmd):
                return False
    return True


def main():
    """Run main."""
    # Give up after a few failures
    tries = 5
    while tries:
        try:
            with open('/dev/powermate', 'rb') as fin:
                # We succeeded, reset our failure count
                tries = 5
                process(fin, volume_callback)
        except OSError as e:
            # Show the error and how many tries are left
            print("{} ({}/{})".format(e, 5 - tries + 1, 5))
            tries -= 1
            if tries:
                # Give the error time to resolve
                time.sleep(2)

    return 0

if __name__ == '__main__':
    main()

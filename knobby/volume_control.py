#!/usr/bin/env python
# coding: utf8
"""<+Module Description.+>"""

from __future__ import division, print_function

import subprocess

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

    while True:
        try:
            with open('/dev/powermate', 'rb') as fin:
                process(fin, volume_callback)
        except OSError:

    return 0

if __name__ == '__main__':
    main()

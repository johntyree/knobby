#!/usr/bin/env python
# coding: utf8
""" A fart button. """

from __future__ import division, print_function

import subprocess

from ..event import EventHandler
from ..main import main


def callback(event):
    if event.name == 'button' and event.data == 1:
        cmd = ['fart']
        if subprocess.call(cmd):
            return 1
    elif event.name == 'turn':
        cmd = ['pulseaudio-ctl']
        cmd.append(('down', 'up')[event.data > 0])
        for i in range(abs(event.data)):
            if subprocess.call(cmd):
                return 1
    return False


fart_handler = EventHandler(callback=callback)

if __name__ == '__main__':
    main(handler=fart_handler)

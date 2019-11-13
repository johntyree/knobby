#!/usr/bin/env python
# coding: utf8
""" A screenlock button.

Just like the volume handlers, but locks the screen instead of muting.
"""

from __future__ import division, print_function

from ..event import EventHandler, EVENT_BUTTON, EVENT_TURN
from ..main import main as root_main
from .skipper import Skipper
from volume_control import VOL_UP, VOL_DOWN


LOCK_CMD = ['cinnamon-screensaver-command', '-l']

handler = Skipper([LOCK_CMD])

def callback(event):
    """ React to a knob event by adjusting the volume or locking. """
    if event.name == EVENT_BUTTON and event.data == 1:
        ret = handler.run(LOCK_CMD)
        if ret:
            return ret
    elif event.name == EVENT_TURN:
        cmd = VOL_UP if event.data > 0 else VOL_DOWN
        for i in range(abs(event.data)):
            handler.run(cmd)
    return False




def main():
    root_main(handler=EventHandler(callback=callback))


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# coding: utf8
""" A fart button.

Just like the volume handlers, but plays a fart noise instead of muting.
"""

from __future__ import division, print_function

from ..event import EventHandler, EVENT_BUTTON, EVENT_TURN
from ..main import main as root_main
from .skipper import Skipper
from volume_control import VOL_UP, VOL_DOWN


handler = Skipper([['fart']])


def fart_callback(event):
    """ React to a knob event by adjusting the volume... or farting. """
    if event.name == EVENT_BUTTON and event.data == 1:
        # assumes you have a fart command... who doesn't?
        ret = handler.run(['fart'])
        if ret:
            return ret
    elif event.name == EVENT_TURN:
        cmd = VOL_UP if event.data > 0 else VOL_DOWN
        for i in range(abs(event.data)):
            handler.run(cmd)
    return False


fart_handler = EventHandler(callback=fart_callback)


def main():
    root_main(handler=fart_handler)


if __name__ == '__main__':
    main()

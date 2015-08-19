#!/usr/bin/env python
# coding: utf8
"""An example script for controlling the system audio with knobby.

Turning the knob left and right increases and decreases the volume. Pressing
the button toggles mute.

"""

from __future__ import division, print_function

from ..event import EventHandler, EVENT_BUTTON, EVENT_TURN
from ..main import main
from .skipper import Skipper

VOL_UP = ['pulseaudio-ctl', 'up']
VOL_DOWN = ['pulseaudio-ctl', 'down']
MUTE = ['pulseaudio-ctl', 'mute']


# We don't want to have to press mute more than once
handler = Skipper([['pulseaudio-ctl mute']])


def volume_callback(event):
    """ React to a knob event by adjusting the volume. """
    if event.name == EVENT_BUTTON and event.data == 0:
        handler.run(MUTE)
    elif event.name == EVENT_TURN:
        cmd = VOL_UP if event.data > 0 else VOL_DOWN
        for i in range(abs(event.data)):
            handler.run(cmd)
    return False


volume_control_handler = EventHandler(callback=volume_callback)

if __name__ == '__main__':
    main(handler=volume_control_handler)

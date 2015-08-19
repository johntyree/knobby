#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import unittest
from os.path import abspath, dirname, join, pardir

from knobby.utils import struct_stream
from knobby.event import (
    Event, EVENT_BY_NAME, EVENT_BUTTON, EVENT_END, EVENT_TURN
)


class TestEvents(unittest.TestCase):

    def setUp(self):
        BUTTON = EVENT_BY_NAME[EVENT_BUTTON]
        END = EVENT_BY_NAME[EVENT_END]
        TURN = EVENT_BY_NAME[EVENT_TURN]

        self.BUTTON_DOWN = Event(0, 0, BUTTON, 1)
        self.BUTTON_UP = Event(0, 0, BUTTON, 0)
        self.END = Event(0, 0, END, 0)
        self.TURN_COUNTERCLOCKWISE = Event(0, 0, TURN, -1)
        self.TURN_CLOCKWISE = Event(0, 0, TURN, 1)

        self.event_table = {
            'D': self.BUTTON_DOWN,
            'U': self.BUTTON_UP,
            'E': self.END,
            'L': self.TURN_COUNTERCLOCKWISE,
            'R': self.TURN_CLOCKWISE,
        }

    def events_from_file(self, fn):
        fn = join(dirname(abspath(__file__)), pardir, 'events', fn)
        events = struct_stream(Event, open(fn, 'rb'))
        return [e.describe() for e in events]

    def events_from_string(self, es):
        return [self.event_table[e].describe() for e in es]

    def test_three_presses(self):
        expected = self.events_from_string("DEUE" * 3)
        result = self.events_from_file('push_button')
        self.assertEqual(result, expected)

    def test_two_presses(self):
        expected = self.events_from_string("DEUE" * 2)
        result = self.events_from_file('two_presses')
        self.assertEqual(result, expected)

    def test_turn_left(self):
        expected = self.events_from_string("LE" * 313)
        result = self.events_from_file('turn_left')
        self.assertEqual(result, expected)

    def test_turn_right(self):
        expected = self.events_from_string("RE" * 111)
        result = self.events_from_file('turn_right')
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
